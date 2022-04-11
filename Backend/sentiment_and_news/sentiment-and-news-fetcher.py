import boto3
from boto3.dynamodb.conditions import Key
import json
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = SentimentIntensityAnalyzer()
bearer_token = 'Bearer Token Here' 
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))
NEWS_KEY = ['news key 1 here', 'news api key 2 here']

dynamodb = boto3.resource('dynamodb')
DYNAMO_TABLE_NAME = 'stocks_sentiment_and_news_table'
table_instance = dynamodb.Table(DYNAMO_TABLE_NAME)

BUCKET_NAME='storeplotsbucket'
s3_client = boto3.client('s3')
IMG_URL ='https://storeplotsbucket.s3.amazonaws.com/' #S3 store URL here


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results = 100):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    #change params based on the endpoint you are using
    query_params = {'query': keyword +' lang:en',
                    'max_results': max_results
                   }
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token = None):
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_polarity(text, combined_pat, nlp):
    text = text.strip()
    if text[:2] == 'RT':
        text = text[2:]
    stripped = re.sub(combined_pat, '', text)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    return nlp.polarity_scores(letters_only.lower())['compound']

def find_sentiment(mn, sf):
    if mn >= .3:
        return 'STRONGLY POSITIVE'
    elif (mn > .1) and (sf > .25):
        return 'STRONGLY POSITIVE'
    elif mn > .1:
        return 'POSITIVE'
    elif (0.05 < mn <= 0.8) and (sf >= 0.25):
        return 'POSITIVE'
    elif (0.05 < mn <= 0.8) and (sf > 0.1):
        return 'MILDY POSITIVE'
    elif  (-.05<=mn<=0.05) and (sf > 0.1) :
        return 'MILDY POSITIVE'  
    elif  -.05<=mn<=0.05:
        return 'NEUTRAL'
    elif  -0.2<mn<-0.05:
        return 'NEGATIVE'
    elif (mn < -0.05) and (sf < -0.2):
        return 'STRONGLY NEGATIVE'
    elif mn < -0.2:
        return 'STRONGLY NEGATIVE'
    else:
        return 'NEUTRAL'
    
def make_detailed_plot(scores,overall_sentiment):
    d =  dict(scores)
    del d['count']
    myList = d.items()
    x, y = zip(*myList)
    plt.figure()
    plt.plot(x, y, 'o-')
    plt.xlabel('Key')
    plt.ylabel('Sentiment value')
    plt.title(overall_sentiment)
    plt.savefig('/tmp/detailed.jpg', bbox_inches='tight', pad_inches=1)
    plt.figure().clear() 
    plt.cla()
    plt.close('all')

def make_variation_plot(dff):
    plt.figure()
    plt.plot(dff)
    plt.savefig('/tmp/variation.jpg', bbox_inches='tight', pad_inches=1)
    plt.cla()
    plt.close('all')

def get_news(news_key, limit, stock_symbol):
    uri = f'https://api.polygon.io/v2/reference/news?ticker={stock_symbol}&limit={limit}&apiKey={news_key}'
    resp = requests.get(uri).json()
    news = []
    count = 0
    for n in range(int(limit)):
        try:
            if count == limit:
                print('news success')
                if news==[]:
                    return ['News cannot be fetched at this point of time.']
                return news
            else:
                news.append(resp['results'][n]['description'])
                count+=1
        except:
            pass
    if news==[]:
        return ['News cannot be fetched at this point of time.']
    return news
    

def update(table_ins, stocksymbol, stocksentiment, stocknews, detailed_plot, variation_plot):
    
    try:
        table_ins.update_item(
            Key={
                    'stock_symbol': stocksymbol,
                },
            UpdateExpression="set stock_news=:n,stock_sentiment=:s,detailed_plot=:d,variation_plot=:v",
            ExpressionAttributeValues={
                    ':n': stocknews,
                    ':s': stocksentiment,
                    ':d' : detailed_plot,
                    ':v' : variation_plot
            },
            ReturnValues="UPDATED_NEW"
            )
        
        print(f'Update success {stocksymbol}')
    except:
        print(f'Update failure {stocksymbol}')


def lambda_handler_getSentiments(event, context):

    for stock_id in range(1,31):
        stock_name = pd.read_csv('./stock_list.csv').loc[int(stock_id)-1,'stock_name']
        stock_symbol = pd.read_csv('./stock_list.csv').loc[int(stock_id)-1,'stock_symbol']
        headers = create_headers(bearer_token=bearer_token)
        url = create_url(keyword=f'{stock_name} lang:en', max_results=100)
        json_response = connect_to_endpoint(url[0], headers, url[1])
        ids = []
        tweets = []
        try:
            datay = json_response.get('data')
            if datay is not None:
                for row in datay:
                    idd, tw = row.values()
                    ids.append(idd)
                    tweets.append(tw)
                df = pd.DataFrame(list(zip(ids, tweets)),columns =['id', 'tweets'])
                df['score'] = df['tweets'].apply(get_polarity, args=(combined_pat, nlp))
                scores = df['score'].describe()
                mn = scores['mean']
                sf = scores['75%']
                overall_sentiment = find_sentiment(mn, sf)
                make_detailed_plot(scores, overall_sentiment)
                make_variation_plot(df['score'])
                print('Plot success')
                s3_client.upload_file('/tmp/variation.jpg', BUCKET_NAME, f'variation_{stock_symbol}.jpg')
                s3_client.upload_file('/tmp/detailed.jpg', BUCKET_NAME, f'detailed_{stock_symbol}.jpg')
                print('uploaded to s3 success')
            else:
                overall_sentiment = 'CANNOT BE FETCHED'
                print('Exception in sentiment', stock_name)
        
        except:
            overall_sentiment = 'CANNOT BE FETCHED'
            print('Exception in sentiment', stock_name)

        try:
            newssamples= get_news(news_key=NEWS_KEY[stock_id-1], limit=2, stock_symbol=stock_symbol)
        except:
            newssamples = 'News cannot be fetched cannot be fetched'
            print('Exception in fetching the news', stock_name)

        update(table_ins=table_instance, stocksymbol=stock_symbol, stocksentiment=overall_sentiment, stocknews=newssamples,detailed_plot=IMG_URL+f'detailed_{stock_symbol}.jpg', variation_plot=IMG_URL+f'variation_{stock_symbol}.jpg')

    print('Completed Execution!')
    return None

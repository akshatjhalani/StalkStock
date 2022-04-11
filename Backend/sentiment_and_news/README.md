## Sentiment and News
This folder contains the service for collecting Tweet post and news, and running sentiment analysis algorithms to get the sentiment results.


### Setup
1. Create a DynamoDB table with name `stocks_sentiment_and_news_table`
2. Create a S3 bucket with name `storeplotsbucket`
3. Create folder in your local, install these packages using pip: matplotlib, pandas, re, requests and vaderSentiment.
4. Create a python file `sentiment_and_news.py` which will basically be your Lambda script file, and set lambda fn name `sentiment_and_news_lambda`
5. Zip this folder and upload to S3 (zip over 50 mb cannot be directly uploaded to Lambda)
6. Upload the code from S3 to Lambda
7. Change the handler name to `sentiment_and_news_lambda.lambda_handler_getSentiments`

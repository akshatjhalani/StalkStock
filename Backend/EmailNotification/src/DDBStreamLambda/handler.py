import psycopg2
import json
#import pandas as pd
import boto3


#################POSTGRES##########
host = r"stock-db.c3nmabp0jl0x.us-east-1.rds.amazonaws.com"
databasename = "postgres"
user = "postgres"
password = "yo%DKUcYfL7PBZ"
port = "5432"
conn = psycopg2.connect(host = host, port= port,user=user, password=password,database=databasename)


###############DYNAMO DB#################


print("started")
def lambda_handler(event,context):
    try:
        
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
               
                new_Image = record['dynamodb']['NewImage']
                
                
                # Reading the Elements in new Image
                # Here ['S'] is for datatype which is string and N for Number
                sym = new_Image['symbol']['S']
                date = new_Image['date']['S']
                close = float(new_Image['close']['S'])
                high = float(new_Image['high']['S'])
                low = float(new_Image['low']['S'])
                open = float(new_Image['open']['S'])
                volume = float(new_Image['volume']['S'])
                cur = conn.cursor()
                
                #reading the data from the postgres db which stores the previous stock prices
                query = "select * from previous_data2 where Symbol = '"+str(sym)+"'"
                cur.execute(query)
                row = cur.fetchone()
                
                if row is None:
                    insert_query = "INSERT INTO previous_data2 VALUES ('"+str(sym)+"',"+str(close)+","+str(high)+","+str(low)+","+str(open)+","+str(volume)+")"
                    cur.execute(insert_query)
                    conn.commit()
                    
                    
                prev_close = float(row[1])
                prev_high = row[2]
                prev_low = row[3]
                prev_open = row[4]
                
                #Calcculating the percent change in the stock prices with the prevois closed prices
                
                print("Calc Percentage Change")
                if close>prev_close:
                    if ((close-prev_close)/prev_close)>=.2:
                        print("Close price increased by 20 percent for the stock ",sym)
                elif close<prev_close:
                    if ((prev_close-close)/prev_close)>=.2:
                        print("Close price decreased by 20 percent for the stock ",sym)
                close = close
                high = 1000
                low = 1000
                open = 1000
                
                #Updating the stock price with the latest closed price
                update_query = "update previous_data2 set previous_close = "+str(close)+" ,previous_high = "+str(high)+" ,previous_low = "+str(low)+" ,previous_open = "+str(open)+" , volume = "+str(volume)+" where symbol = '"+str(sym)+"'"     
                cur.execute(update_query)
                conn.commit()
                
                
                
                sns_client= boto3.client("sns")
                if sym == 'TEST':
                    topicArn = 'arn:aws:sns:us-east-1:555178539686:TEST1'
                    if close>prev_close:
                        if ((close-prev_close)/prev_close)>=.2:
                            print("Sending email for the stock",sym)
                            subject = 'Stock price has gone up by 20 percent for the stock '+str(sym)
                            message = 'Stock name : '+str(sym)+"\n"+"Previous Price : "+str(prev_close)+"\n"+"Current Price : "+str(close)+"\n Date and Time : "+str(date)
                            response = sns_client.publish(TopicArn = topicArn,
                            Message = message,
                            Subject = subject)
                            
                            
                if sym == 'TEST2':
                    topicArn = 'arn:aws:sns:us-east-1:555178539686:TEST2'
                    if close>prev_close:
                        if ((close-prev_close)/prev_close)>=.2:
                            subject = 'Stock price has gone up by 20 percent for the stock '+str(sym)
                            message = 'Stock name : '+str(sym)+"\n"+"Previous Price : "+str(prev_close)+"\n"+"Current Price : "+str(close)+"\n Date and Time : "+str(date)
                            response = sns_client.publish(TopicArn = topicArn,
                            Message = message,
                            Subject = subject)                            
                            
                #print(update_query)
    except Exception as e:
        print(e)
    
    

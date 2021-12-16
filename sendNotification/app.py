from os import environ
import json
import requests
import boto3
from botocore.exceptions import ClientError


api_key = environ.get("TELEGRAM_API_KEY")
telegram_api_key = environ.get("TELEGRAM_API_KEY")
twitter_token = environ.get("TWITTER_TOKEN")
account_id = environ.get("ACCOUNT_ID")
table_name = environ.get("TABLE_NAME")
general_chat_id = environ.get("GENERAL_CHAT_ID")
alerts_chat_id = environ.get("ALERTS_CHAT_ID")
table = boto3.resource('dynamodb').Table(table_name)

def get_last_tweet_id():
    try:
        response = table.get_item(Key={'key': "newest_tweet_id"})
        print(response)
    except ClientError as e:
        print("error at get_last_tweet_id")
        print(e.response['Error']['Message'])
        return False
    else:
        return response['Item']['value'] if "Item" in response else False


def update_last_tweet_id(id):
    upserted_item = {'key': "newest_tweet_id", 'value': id}
    try:
        table.put_item(Item=upserted_item)
    except ClientError as e:
        print("error at update_last_tweet_id")
        print(e.response['Error']['Message'])
        return False
    else:
        return upserted_item


def exist_in_str(substrings, str):
    return True in [
        str.lower().__contains__(substr.lower()) for substr in substrings
    ]


def send_telegram(chat_id, message):
    return requests.post(
        f"https://api.telegram.org/bot{telegram_api_key}/sendMessage",
        json={
            'chat_id': chat_id,
            'text': message,
            'disable_web_page_preview': True
        })

def get_tweets(since_id = False):
    request_args = {
            'url':
            f"https://api.twitter.com/2/users/966681992367693824/tweets",
            'headers': {
                'Authorization': f"Bearer {twitter_token}"
            },
        }

    if since_id:
        request_args['params'] = {'since_id': since_id}

    twitter_response = requests.get(**request_args)

    result = twitter_response.json()

    count = result["meta"]["result_count"] if not "errors" in result else False

    return [result, count]


def lambda_handler(event, context):
    try:
        last_twitter_id = get_last_tweet_id()

        result, count = get_tweets(last_twitter_id)

        if count:
            for entry in result["data"]:
                message = f"""{entry["text"]}

https://twitter.com/i/web/status/{entry['id']}"""

                print(message)

                send_telegram(chat_id=general_chat_id, message=message)

                if exist_in_str([
                        "aviso", "avviso", "prenota", "turno", "importante",
                        "ciudadanía", "cittadinanza", "partida"
                ], message):
                    print("sending alert")
                    send_telegram(chat_id=alerts_chat_id, message=message)

            update_last_tweet_id(result["meta"]["newest_id"])

        else:
            print("no new tweets")

    except NameError:
        print("Error at main")
        print(NameError)
    except Exception as error:
        print("Error at main")
        print(error)

    return {
        "statusCode": 200,
        "body": "finished",
    }
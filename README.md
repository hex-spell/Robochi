# Robochi
## Test local
 - `. /local-test sendNotification`

## Test remote
 - `. /remote-test sendNotification`

## Deploy
 - `. /deploy`

## Environment variables
 - `TELEGRAM_API_KEY`: Telegram api key (bot)
 - `TWITTER_TOKEN`: Twitter token (bearer token)
 - `TABLE_NAME`: Dynamo db table name (the key of the table must be called "key" and be a string)
 - `ACCOUNT_ID`: Twitter account id to watch (numeric id)
 - `GENERAL_CHAT_ID`: General chat id (telegram) (unfiltered messages)
 - `ALERTS_CHAT_ID`: Alerts chat id (telegram)

## TODO
 - Google translation on the fly
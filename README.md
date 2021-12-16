# Robochi
| <b>Ho fatto un Roboci, mira sei tu</b> |
| :------------------------------------: |
|      ![space-1.jpg](robochi.png)       |

I use this bot to get filtered twitter notifications from a specific account without using Twitter

Me don't like Twitter

It stays within the **aws free tier**, if you deploy it yourself it will be free to use forever (as far as I've calculated)

## Must know

- Scripts are written for linux shell, I haven't tried running them on windows or mac

### For the deploy and tests to work you must have installed

- aws cli
- aws sam cli
- your aws credentials and configuration in ~/.aws folder (the user will need resources and roles creation permission)
- telegram bot, and its token
- twitter app, and its token
- dynamodb table
- 2 telegram chat ids (@name if they are public, or id number if they are private)
- setenv file (use setenv.example to see how to make it)

## Test local

- `. local-test sendNotification`

## Test remote

- `. remote-test sendNotification`

## Deploy

- `. deploy`

## Environment variables

- `TELEGRAM_API_KEY`: Telegram api key (bot)
- `TWITTER_TOKEN`: Twitter token (bearer token)
- `TABLE_NAME`: Dynamo db table name (the key of the table must be called "key" and be a string)
- `ACCOUNT_ID`: Twitter account id to watch (numeric id)
- `GENERAL_CHAT_ID`: General chat id (telegram) (unfiltered messages)
- `ALERTS_CHAT_ID`: Alerts chat id (telegram)

## TODO

- Google translation on the fly
- Clean requirements.txt
- Make dynamodb table creation automatic from prebuild.yaml template resources


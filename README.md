# secondbrain

Integrated with Telegram.

## Build index with llama-index
```
# Index build script not yet integrated with this code base.
```

## Build app with AWS SAM
```
sam build
```

## Test with local invoke
```
sam local invoke InferenceFunction --event events/event.json --parameter-overrides TeleToken=<TELEGRAM_TOKEN> OpenAIKey=<OPENAI_API_KEY> AllowedTeleUser=<TELEGRAM_USER_ID>
```

## Deploy
```
sam deploy
```


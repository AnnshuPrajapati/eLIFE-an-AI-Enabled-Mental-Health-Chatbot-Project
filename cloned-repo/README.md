# Jokebot - Rasa Demo Bot

This is a Rasa demo bot. You can try the bot out at [https://avkana.com/jokebot](https://avkana.com/jokebot).

You can ask for Geek jokes, Corny jokes. Also, Kanye, Ron Swanson, Creed, Breaking Bad, Inspiring or Trump quotes.

## ToDo

- Brainy quote, `https://github.com/Hemil96/Brainyquote-API`
- Github Actions pipeline
- Google Assistant integration
- NLU test data
- Core test data
- rasa validate
- Support [multi-intents](https://blog.rasa.com/how-to-handle-multiple-intents-per-input-using-rasa-nlu-tensorflow-pipeline/?_ga=2.50044902.1771157212.1575170721-2034915719.1563294018)

## New Features

**Oct 2022**

- Upgrade to 3.0

**Jan 2021:**

- GitHub actions
  - Build actions docker image
- Creed quotes
- Kanye quotes, `https://api.kanye.rest/?format=text`

## Test Curl

```
curl --location --request POST 'http://localhost:5055/webhook' \
--data-raw '{      
  "next_action": "action_kanye",
  "sender_id": "postman",
  "tracker": {
    "sender_id": "default",
    "slots": {},
    "latest_message": {},
    "latest_event_time": 1535092548.4191391,
    "followup_action": "action_listen",
    "events": []
  },
  "domain": {
    "config": {},
    "intents": [],
    "entities": [],
    "slots": {}
  }
}'
```

```
curl --location --request POST 'http://rasa-production:5005/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
curl --location --request POST 'http://localhost/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
```
# Tech news bot
 Telegram bot that scraps the web to keep users informed with the latests tech news on their selected topics.
 
 Functional instance running at [@Bamm_bamm_bot](https://t.me/bamm_bamm_bot)
 
 ## Usage

Create `credentials/credentials.py` from root. Add bot token and neo4j connection data:
```angular2
token = 'token'

NEO4J_CONN = 'bolt://neo4j:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASS = '1234'
```

Add your scrappers to `bot/scrapper.py`. Dummy examples are added as indication.

#### Running locally
Launch neo4j instance: 
 - Get `neo4j-community` ([relevant](https://stackoverflow.com/questions/26395551/error-running-neo4j-with-systemd-on-arch-linux) for Arch users)
- From `neo4j-community/` execute:
```
systemctl start neo4j-service
```

Launch the bot:
```angular2
python run.py
```

#### Running on docker
```angular2
docker-compose build
docker-compose run
```



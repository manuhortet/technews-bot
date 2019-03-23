# Bamm-Bamm bot
 Telegram bot that scraps the web to keep users informed with the latests tech news on their selected topics.
 
 [@Bamm_bamm_bot](https://t.me/bamm_bamm_bot)
 
 ## Usage

Create `credentials/credentials.py` from root. Add bot token and neo4j connection data.

Launch neo4j instance: 
 - Get `neo4j-community` ([relevant](https://stackoverflow.com/questions/26395551/error-running-neo4j-with-systemd-on-arch-linux) for arch users)
- From `neo4j-community/` execute:
```
systemctl start neo4j-service
```

Add your scrappers to `bot/scrapper.py`. Dummy example is added as `scrap_techcrunch()`



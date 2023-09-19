# OLX Odessa New Goods Parser
---
.env file (MODE=DEV or MODE=PROD):
```
BOT_TOKEN
MODE
```

run app:

```
docker build -t olx_odessa_parser . && docker run -it olx_odessa parser
```
# GetAround API

Bienvenue sur cette application API. Il y a 2 endpoints:

1. `/data` qui fournit les données brutes
2. `/predictions` qui prédit le prix d'une location de voiture

## Deploy FastAPI to Docker 

Heroku utilise WSGI web server framework alors que FastAPI utilise ASGI. Il faut mettre dans le Dockerfile ce genre de commande :

`gunicorn api:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker`

More info here: https://stackoverflow.com/questions/63424042/call-missing-1-required-positional-argument-send-fastapi-on-app-engine/70404102#70404102


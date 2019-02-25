# fartor

Fartot is a modern, highly engineered and highly customizable Instagram-like platform that is crafted with best technologies.

## Stack

- Django
- React / Material UI
- Postgres 
- Redis
- Celery
- Graphql / Django Rest Framework
- Docker / Docker compose / Alpine images
- OneSignal
- Nginx
- Daphne

## Setup

You can quickly setup and run fartor using docker compose

First rename `.env.sample` to `.env`

Then set your environment variables.


After that, run fartor using docker compose:


```bash
docker-compose up -d web db redis
```

Do NOT use this in a production environment, I'll add documents for deploying fartor later.

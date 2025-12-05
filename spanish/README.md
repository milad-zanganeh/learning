## Spanish Dict Bot

A tiny bot that scrapes `spanishdict.com` vocabulary lists and posts one new word (with example sentences) to a Telegram channel on a fixed daily schedule.

### Requirements

- Docker and Docker Compose

### Configurations
Create config.py file and add your configurations:

```bash
cp app/config.py.sample app/config.py
vim app/config.py
```

### How to run

```bash
docker compose up -d --build
```

This starts a container that:

- Uses the Europe/Madrid timezone
- Stores its SQLite DB in the local `data/` directory
- Runs an internal Python scheduler that sends at the configured times in `app/config.py`.

### Stopping

```bash
docker compose down
```



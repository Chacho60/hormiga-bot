# Hormiga Bot

## Description

Python bot that uses LLM to analyze expenses.

<aside>
💡 In order to use the bot you’ll need to also fire up the [hormiga-connector](https://github.com/Chacho60/hormiga-connector) service, which allows the bot to communicate with telegram.

</aside>

## Table of Contents

1. [I](notion://www.notion.so/e05e48ba377d4949ac43a8d3b81abb50?showMoveTo=true&saveParent=true#installation)nstallation
2. Configuration
3. Usage

## Installation

To install the Hormiga Bot, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/Chacho60/hormiga-bot.git
cd hormiga-bot
```

1. Create a virtual environment:

```
pip install virtualenv
virtualenv venv
```

1. Activate virtual environment

```
source venv/bin/activate
```

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

1. Set up the environment variables by copying the `.env example` file to `.env` and filling in the required values. The example already has default values for a local environment installation, however, bear in mind the example doesn’t have an Open AI key, so a key should be provided.
2. (OPTIONAL) Start the docker-compose file to fire up the postgres database and rabbitmq local server, this is already linked to the env variables of the env.example:

```json
docker-compose up
```

1. Run the bot:

```bash
python src/main.py
```

## Configuration

Configure your environment variables in the `.env` file:

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
QUEUE_URL=
OPEN_API_KEY=
OUTGOING_QUEUE=
INCOMING_QUEUE=
```

## Overview

This python bot makes use of langchain to leverage the power of LLM’s, the bot will consume messages from a rabbitmq queue and analyze those messages in order to insert any expense message in a postgres db.

Postgres is not only used for user management and expense records, it also hosts prompt templates which will be fed to the LLM to make the queries that will analyze the messages. This approach allows to have a better organization, scalability and makes easy to add new LLM features in the future.

To use your own bot, you just have to create a new telegram bot and add the key to the .env file.

Also, a live version of the bot hosted in railway, supbase and cloudamqp is available at https://t.me/chacho_ant_bot

## Usage

Once the bot is running, you can interact with it on Telegram by sending any message, at first the bot will tell you to register and then you’ll just start sending it your expenses.

- `/start` - Start the bot
- `/register` - Register your user, only once

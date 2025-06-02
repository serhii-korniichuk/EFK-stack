# EFK Stack + Telegram Logger Bot

This repository combines an **EFK stack (Elasticsearch + Fluentd + Kibana)** for centralized logging with a **Telegram bot** that sends messages as logs into the system.

> Base EFK stack: https://github.com/giefferre/EFK-stack  

## 📦 Components

- **Elasticsearch** — stores logs in a structured format.
- **Fluentd** — receives HTTP requests, parses logs, and forwards them to Elasticsearch.
- **Kibana** — provides an interface for viewing and analyzing logs.
- **Telegram Logger Bot** — a bot that receives messages from users and sends them to Fluentd.

## 🚀 How to Run

### 1. Configure environment variables

Create a `.env` file for the bot:

```
BOT_TOKEN=your_telegram_bot_token
FLUENTD_ENDPOINT=http://localhost:8080
```

### 2. Launch EFK stack

```bash
docker-compose up
```

The EFK stack will be available at:
- Kibana: http://localhost:5601
- Fluentd HTTP endpoint: http://localhost:8080

### 3. Run the bot

```bash
python3 telegram_logger.py
```

## 🔁 Interaction Flow

1. A user sends a message to the Telegram bot.
2. The bot creates a JSON log:
```json
{
  "@timestamp": "2025-05-31T22:08:23Z",
  "type": "telegram_message",
  "user_id": 12345678,
  "username": "username",
  "message": "sample message"
}
```
3. The log is sent to Fluentd via HTTP (`http://localhost:8080`).
4. Fluentd forwards the log to Elasticsearch.
5. The log is available in Kibana under the Discover section.

## 📊 Kibana Visualization

- Go to Discover → filter by `type: telegram_message`
- Build activity charts: Visualize → Bar Chart → use the `@timestamp` field
- Optional: create user activity visualizations by `username`

## 🧪 Testing

- Send a message to the bot
- Check if it appears in Kibana → Discover
- Or test manually:
```bash
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"@timestamp":"2025-05-31T22:00:00Z","type":"test","message":"Hello from curl!"}'
```

## 📚 Purpose

This project demonstrates how to:
- implement centralized logging
- integrate a Telegram bot with Fluentd
- visualize messages in Kibana
- use the EFK stack to collect logs from any service

## 📄 License

MIT License

# Telegram VPN Service

Production-ready starter for a Telegram Mini App + FastAPI backend + aiogram bot.

## Features

- Telegram WebApp authentication with signature validation
- JWT sessions for API access
- Devices management with rate limiting
- Mock balance top-up
- 3X-UI API integration wrapper
- Docker + docker-compose setup

## Project Structure

```
app/                # FastAPI backend
  core/             # config, security, rate limiting
  routes/           # API endpoints
  services/         # 3X-UI integration
bot/                # Telegram bot (aiogram 3)
web/                # Mini App HTML/JS
```

## Environment Variables

Create a `.env` file in the repo root:

```
BOT_TOKEN=your-telegram-bot-token
JWT_SECRET=change-me
WEB_APP_URL=https://your-domain-or-ngrok
THREE_X_UI_BASE_URL=http://3x-ui:2053
THREE_X_UI_USERNAME=admin
THREE_X_UI_PASSWORD=admin
```

## Running locally

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Mini App: http://localhost:8080

## API Endpoints

- `POST /auth` (form field: `init_data`)
- `GET /me`
- `GET /devices`
- `POST /devices`
- `DELETE /devices/{id}`
- `POST /balance/topup`

## Notes

- The bot only sends the "Open VPN App" WebApp button.
- The Mini App sends Telegram `initData` for validation.
- Rate limiting is in-memory; use Redis for production.

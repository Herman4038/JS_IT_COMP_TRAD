# JS IT COMP TRAD - Django Project

A Django project containerized with Docker and PostgreSQL.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd JS_IT_COMP_TRAD
   ```

2. **Build and run the containers**
   ```bash
   docker-compose up --build
   ```

3. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Populate with sample data**
   ```bash
   docker-compose exec web python manage.py populate_sample_data
   ```

5. **Create a superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - Django Admin: http://localhost:8000/admin/
   - Main site: http://localhost:8000/
   - Frontend: Open `frontend/index.html` in your browser

## Project Structure

```
JS_IT_COMP_TRAD/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                 # Docker image configuration
├── requirements.txt           # Python dependencies
├── manage.py                 # Django management script
├── js_it_comp_trad/          # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── backend/                  # Backend Django apps
│   ├── __init__.py
│   └── trading/             # Trading application
│       ├── __init__.py
│       ├── models.py        # Database models
│       ├── views.py         # API views and endpoints
│       ├── admin.py         # Django admin configuration
│       └── management/      # Management commands
│           └── commands/
│               └── populate_sample_data.py
├── frontend/                # Frontend static files
│   ├── index.html          # Main trading platform page
│   ├── styles.css          # Custom CSS styles
│   └── script.js           # JavaScript functionality
└── .dockerignore           # Files to exclude from Docker build
```

## Docker Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)

## Volumes

- `postgres_data`: Persistent PostgreSQL data
- `static_volume`: Static files
- `media_volume`: Media files

## Environment Variables

Create a `.env` file in the root directory with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_DB=js_it_comp_trad
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Useful Commands

```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Run Django management commands
docker-compose exec web python manage.py [command]

# Access Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic
```

## Features

### Backend (Django)
- **Portfolio Management**: Track user portfolios and holdings
- **Trading System**: Execute buy/sell trades with validation
- **Market Data**: Real-time asset prices and historical data
- **Watchlist**: Add assets to personal watchlist
- **Alerts**: Set price alerts for assets
- **Admin Interface**: Full Django admin for data management

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Responsive design with Bootstrap 5
- **Interactive Charts**: Real-time price charts using Chart.js
- **Trading Interface**: Buy/sell forms with validation
- **Portfolio Dashboard**: View holdings and performance
- **Market Overview**: Live market data display
- **Analytics**: Performance metrics and risk analysis

## Development

The project is set up for development with:
- Hot reloading (code changes are reflected immediately)
- PostgreSQL database with persistent data
- Static and media file serving
- Debug mode enabled
- Sample data for testing

## Sample Data

After running the populate command, you'll have:
- Sample user: `trader` (password: `password123`)
- Sample assets: BTC, ETH, SPY, TSLA, AAPL, GOOGL, MSFT, AMZN, NVDA, META
- Sample portfolio with holdings and trade history
- 30 days of historical market data 
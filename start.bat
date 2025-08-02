@echo off
echo 🚀 Starting JS IT COMP TRAD Application...

REM Stop any existing containers (without removing volumes)
echo 📦 Stopping existing containers...
docker-compose down

REM Build and start containers
echo 🔨 Building and starting containers...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Check if containers are running
echo 🔍 Checking container status...
docker-compose ps

echo.
echo ✅ Application is starting up!
echo 🌐 Access your application at: http://localhost:8000
echo 🔑 Default superuser credentials: admin / admin123
echo.
echo 📋 Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Stop containers: docker-compose down
echo   - Stop and remove volumes: docker-compose down -v (⚠️  WARNING: This will delete all data!)
echo.
pause 
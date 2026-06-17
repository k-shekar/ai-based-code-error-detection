# Setup Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Node.js 18+ (for JavaScript analysis)
- Java 17+ (for Java analysis)
- Git

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-code-error-detection
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **Verify installation**
   ```bash
   curl http://localhost:8000/health
   ```

## Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js tools**
   ```bash
   npm install -g eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
   ```

4. **Set up database**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d db redis
   
   # Run migrations
   alembic upgrade head
   ```

5. **Download ML models**
   ```bash
   python scripts/download_models.py
   ```

6. **Start the application**
   ```bash
   python -m src.main
   ```

## Configuration

Create a `.env` file in the project root:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/codeanalysis
REDIS_URL=redis://localhost:6379

# ML Models
MODEL_PATH=./models
ENABLE_ML_ANALYSIS=true

# Security
API_KEY=your-secret-api-key
RATE_LIMIT_REQUESTS=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

## API Usage

### Analyze Code

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello World\")",
    "language": "python",
    "file_path": "example.py"
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## IDE Integration

### VS Code Extension

1. Install the extension from the marketplace
2. Configure the server URL in settings:
   ```json
   {
     "aiCodeAnalysis.serverUrl": "http://localhost:8000",
     "aiCodeAnalysis.apiKey": "your-api-key"
   }
   ```

### IntelliJ Plugin

1. Download the plugin JAR file
2. Install via Settings → Plugins → Install from disk
3. Configure server settings in the plugin preferences

## Monitoring

Access monitoring dashboards:

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Memory issues**: Increase Docker memory allocation
3. **Model loading fails**: Check MODEL_PATH and download models
4. **Database connection**: Verify PostgreSQL is running

### Logs

Check application logs:
```bash
docker-compose logs api
tail -f logs/app.log
```

### Performance Tuning

- Adjust worker processes in docker-compose.yml
- Configure Redis memory limits
- Optimize ML model batch sizes in config.py
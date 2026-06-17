# CodeGuard AI - Deployment Guide

## Quick Start

### Local Development
```bash
# Clone and navigate to project
cd ai-code-error-detection/src

# Install dependencies
pip install fastapi uvicorn

# Run the application
python main_simple.py

# Access the application
# Web Interface: http://localhost:8001
# API Documentation: http://localhost:8001/docs
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services
# Application: http://localhost:8001
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## Production Deployment

### Environment Variables
```env
# Server Configuration
HOST=0.0.0.0
PORT=8001
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379

# Security
API_KEY=your-secure-api-key
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600

# ML Models
MODEL_PATH=/app/models
ENABLE_ML_ANALYSIS=true
ENABLE_SECURITY_SCAN=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codeguard-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codeguard-ai
  template:
    metadata:
      labels:
        app: codeguard-ai
    spec:
      containers:
      - name: api
        image: codeguard-ai:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Load Balancer Configuration
```nginx
upstream codeguard_backend {
    server app1:8001;
    server app2:8001;
    server app3:8001;
}

server {
    listen 80;
    server_name codeguard.example.com;
    
    location / {
        proxy_pass http://codeguard_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /api/ {
        proxy_pass http://codeguard_backend;
        proxy_set_header Content-Type application/json;
        client_max_body_size 10M;
    }
}
```

## Monitoring Setup

### Prometheus Configuration
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'codeguard-api'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
```

### Grafana Dashboard
- Import dashboard ID: 12345
- Configure data source: Prometheus
- Set up alerts for response time > 2s
- Monitor error rates and throughput

## Security Checklist

- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure API rate limiting
- [ ] Set up authentication and authorization
- [ ] Enable request/response logging
- [ ] Configure firewall rules
- [ ] Set up intrusion detection
- [ ] Enable automated security updates
- [ ] Configure backup and disaster recovery

## Performance Optimization

### Database Tuning
```sql
-- PostgreSQL optimizations
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

### Redis Configuration
```conf
# redis.conf optimizations
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Application Tuning
- Enable response compression
- Configure connection pooling
- Implement result caching
- Optimize ML model loading
- Use async processing for large files

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port
netstat -tulpn | grep :8001
# Kill process
kill -9 <PID>
```

**Database Connection Failed**
```bash
# Check database status
pg_isready -h localhost -p 5432
# Test connection
psql -h localhost -U user -d database
```

**High Memory Usage**
```bash
# Monitor memory usage
htop
# Check application logs
tail -f logs/app.log
# Restart application
systemctl restart codeguard-ai
```

**Slow Analysis Performance**
- Check CPU usage during analysis
- Monitor database query performance
- Verify ML model loading times
- Review code complexity metrics

### Log Analysis
```bash
# View application logs
tail -f /app/logs/app.log

# Search for errors
grep "ERROR" /app/logs/app.log

# Monitor API requests
grep "POST /api/v1/analyze" /app/logs/app.log | tail -20

# Check performance metrics
grep "analysis_time" /app/logs/app.log | awk '{print $NF}' | sort -n
```

## Backup and Recovery

### Database Backup
```bash
# Create backup
pg_dump -h localhost -U user database > backup.sql

# Restore backup
psql -h localhost -U user database < backup.sql
```

### Application Backup
```bash
# Backup configuration
tar -czf config-backup.tar.gz .env docker-compose.yml

# Backup ML models
tar -czf models-backup.tar.gz models/

# Backup logs
tar -czf logs-backup.tar.gz logs/
```

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple application instances
- Use load balancer for traffic distribution
- Implement session affinity if needed
- Configure shared storage for models

### Vertical Scaling
- Increase CPU cores for faster analysis
- Add more RAM for larger codebases
- Use SSD storage for better I/O performance
- Optimize database server resources

### Auto-scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: codeguard-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: codeguard-ai
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Support and Maintenance

### Regular Maintenance Tasks
- Update dependencies monthly
- Review and rotate API keys quarterly
- Analyze performance metrics weekly
- Update ML models as needed
- Review security logs daily

### Health Checks
```bash
# Application health
curl http://localhost:8001/health/

# Database health
pg_isready -h localhost -p 5432

# Redis health
redis-cli ping

# System resources
df -h && free -h && uptime
```

### Update Procedure
1. Backup current deployment
2. Test updates in staging environment
3. Deploy during maintenance window
4. Verify all services are running
5. Monitor for issues post-deployment
6. Rollback if necessary

For additional support, refer to the project documentation or contact the development team.
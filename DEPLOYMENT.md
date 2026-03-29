# NeuroWall Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose
- Domain name (optional, for production)
- SSL certificates (for HTTPS)
- PostgreSQL database (managed or self-hosted)
- Redis instance (managed or self-hosted)

### Environment Variables

#### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/neurowall

# Security
SECRET_KEY=<generate-strong-secret-key>
AGENT_SECRET_KEY=<generate-strong-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://host:6379/0

# gRPC
GRPC_PORT=50051
GRPC_CERT_PATH=./certs/server.crt
GRPC_KEY_PATH=./certs/server.key
GRPC_CA_PATH=./certs/ca.crt

# ML Configuration
ML_WINDOW_SIZE=1000
ML_Z_SCORE_THRESHOLD=2.5
```

#### Dashboard (.env.local)

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

### Docker Compose Production

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: neurowall
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      SECRET_KEY: ${SECRET_KEY}
      AGENT_SECRET_KEY: ${AGENT_SECRET_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    ports:
      - "8000:8000"

  celery:
    build: ./backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    command: celery -A app.celery_app worker --loglevel=info --concurrency=4

  dashboard:
    build: ./dashboard
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL}
      NEXT_PUBLIC_WS_URL: ${NEXT_PUBLIC_WS_URL}
    restart: unless-stopped
    ports:
      - "3000:3000"

volumes:
  postgres_data:
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/neurowall

upstream backend {
    server localhost:8000;
}

upstream dashboard {
    server localhost:3000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/TLS Setup

Use Let's Encrypt with Certbot:

```bash
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

### Agent Deployment

#### Windows Agent

1. Build the agent:
```bash
cd agent/windows
cargo build --release
```

2. Create service (using NSSM or Windows Service):
```powershell
# Install as Windows Service
nssm install NeuroWallAgent "C:\path\to\neurowall-agent-windows.exe"
nssm set NeuroWallAgent AppDirectory "C:\path\to\config"
nssm start NeuroWallAgent
```

3. Configuration file (`config.json`):
```json
{
  "device_id": "windows-workstation-001",
  "server_url": "https://api.yourdomain.com",
  "grpc_endpoint": "https://api.yourdomain.com:50051",
  "api_endpoint": "https://api.yourdomain.com/api/v1",
  "policy_cache_path": "C:\\ProgramData\\NeuroWall\\policy_cache.json",
  "heartbeat_interval_secs": 30,
  "telemetry_batch_size": 100,
  "telemetry_flush_interval_secs": 5
}
```

#### Linux Agent

1. Build the agent:
```bash
cd agent/linux
cargo build --release
```

2. Create systemd service (`/etc/systemd/system/neurowall-agent.service`):
```ini
[Unit]
Description=NeuroWall Agent
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/neurowall-agent-linux
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl enable neurowall-agent
sudo systemctl start neurowall-agent
```

4. Configuration file (`/etc/neurowall/config.json`):
```json
{
  "device_id": "linux-server-001",
  "server_url": "https://api.yourdomain.com",
  "grpc_endpoint": "https://api.yourdomain.com:50051",
  "api_endpoint": "https://api.yourdomain.com/api/v1",
  "policy_cache_path": "/var/lib/neurowall/policy_cache.json",
  "heartbeat_interval_secs": 30,
  "telemetry_batch_size": 100,
  "telemetry_flush_interval_secs": 5
}
```

### Database Migrations

If using Alembic:

```bash
cd backend
alembic upgrade head
```

### Monitoring

#### Health Checks

- Backend: `GET /health`
- Database: PostgreSQL connection check
- Redis: `redis-cli ping`

#### Logging

Configure centralized logging:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Loki + Grafana
- Cloud logging services

### Backup Strategy

1. **Database Backups:**
```bash
# Daily backup script
pg_dump -U neurowall neurowall > backup_$(date +%Y%m%d).sql
```

2. **Policy Cache Backups:**
- Agents maintain local cache
- Backend stores policies in database

3. **Configuration Backups:**
- Version control for configuration files
- Encrypted secrets management

### Scaling

#### Horizontal Scaling

1. **Backend API:**
   - Deploy multiple instances
   - Use load balancer
   - Ensure stateless design

2. **Celery Workers:**
   - Add more worker processes
   - Scale based on queue depth

3. **Database:**
   - Read replicas for queries
   - Connection pooling

#### Vertical Scaling

- Increase database resources
- Increase Redis memory
- Optimize query performance

### Security Hardening

1. **Network Security:**
   - Firewall rules
   - VPN for agent communication
   - Network segmentation

2. **Application Security:**
   - Regular security updates
   - Dependency scanning
   - Penetration testing

3. **Secrets Management:**
   - Use secret management services
   - Rotate keys regularly
   - Encrypt at rest

### Troubleshooting

#### Common Issues

1. **Agent Not Connecting:**
   - Check network connectivity
   - Verify firewall rules
   - Check agent logs

2. **High CPU Usage:**
   - Review agent configuration
   - Check ML processing load
   - Optimize database queries

3. **Memory Issues:**
   - Review baseline window sizes
   - Optimize telemetry retention
   - Increase resources if needed

### Maintenance

#### Regular Tasks

- Database maintenance (vacuum, analyze)
- Log rotation
- Certificate renewal
- Security updates
- Performance monitoring

---

**Last Updated:** 2024


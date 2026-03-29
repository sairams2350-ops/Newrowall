# NeuroWall Quick Start Guide

Get NeuroWall up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 3000, 8000, 5432, 6379 available

## Step 1: Clone and Start

```bash
# Navigate to project directory
cd neurowall

# Start all services
docker-compose up -d

# Wait for services to start (30-60 seconds)
docker-compose logs -f
```

## Step 2: Access the Dashboard

Open your browser and navigate to:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## Step 3: Create Admin User

```bash
# Register admin user via API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "is_admin": true
  }'
```

## Step 4: Login

1. Go to http://localhost:3000/login
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`

## Step 5: Create Your First Rule

1. Click on "Rules" in the sidebar
2. Click "+ New Rule"
3. Fill in:
   - Name: "Block Example Domain"
   - Scope: Global
   - Action: Deny
   - Domain: example.com
4. Click "Create Rule"

## Step 6: (Optional) Deploy an Agent

### Windows Agent

```powershell
# Build agent
cd agent\windows
cargo build --release

# Create config.json
# Edit config.json with your backend URL

# Run agent (as Administrator)
.\target\release\neurowall-agent-windows.exe
```

### Linux Agent

```bash
# Build agent
cd agent/linux
cargo build --release

# Create config.json
# Edit config.json with your backend URL

# Run agent (as root)
sudo ./target/release/neurowall-agent-linux
```

## Verify Everything Works

1. **Check Backend Health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Dashboard:**
   - Navigate to http://localhost:3000
   - You should see the dashboard

3. **Check Services:**
   ```bash
   docker-compose ps
   ```
   All services should show "Up"

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Review [AGENT_SETUP.md](AGENT_SETUP.md) for agent deployment
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose up --build
```

### Can't Access Dashboard

- Verify port 3000 is not in use
- Check firewall settings
- Review docker-compose logs

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
docker-compose exec postgres psql -U neurowall -d neurowall
```

## Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

---

**That's it!** You now have NeuroWall running. Start creating rules and monitoring your network!


# Step-by-Step Instructions to Run NeuroWall

## Prerequisites Check

Before starting, ensure you have:
- Docker Desktop installed and running
- Docker Compose installed
- At least 4GB RAM available
- Ports 3000, 8000, 5432, 6379 available

## Step 1: Verify Docker is Running

```bash
# Check Docker is running
docker --version
docker-compose --version

# If Docker Desktop is not running, start it first
```

## Step 2: Navigate to Project Directory

```bash
# You should already be in D:\neurowall
# Verify you're in the right directory
cd D:\neurowall
dir
```

You should see:
- `backend/` folder
- `dashboard/` folder
- `agent/` folder
- `ml/` folder
- `docker-compose.yml` file

## Step 3: Create Environment File (Optional but Recommended)

```bash
# Create backend .env file if it doesn't exist
copy backend\.env.example backend\.env
```

Edit `backend\.env` if needed (defaults should work for local development).

## Step 4: Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# This will:
# - Pull/download required images
# - Build custom images
# - Start PostgreSQL, Redis, Backend, Celery, Dashboard
```

**Expected Output:**
```
Creating network "neurowall_default" ...
Creating neurowall_postgres_1 ...
Creating neurowall_redis_1 ...
Creating neurowall_backend_1 ...
Creating neurowall_celery_1 ...
Creating neurowall_dashboard_1 ...
```

## Step 5: Wait for Services to Start

```bash
# Check service status
docker-compose ps
```

Wait until all services show "Up" status (may take 30-60 seconds).

**Expected Output:**
```
NAME                    STATUS
neurowall_postgres_1    Up
neurowall_redis_1       Up
neurowall_backend_1      Up
neurowall_celery_1      Up
neurowall_dashboard_1    Up
```

## Step 6: View Logs (Optional)

```bash
# View all logs
docker-compose logs -f

# Or view specific service logs
docker-compose logs -f backend
docker-compose logs -f dashboard
```

Press `Ctrl+C` to exit log view.

## Step 7: Verify Backend API is Running

Open your browser or use curl:

```bash
# Test backend health
curl http://localhost:8000/health

# Or open in browser:
# http://localhost:8000/health
```

**Expected Output:**
```json
{"status": "healthy"}
```

## Step 8: Access API Documentation

Open in browser:
```
http://localhost:8000/docs
```

You should see the Swagger UI with all API endpoints.

## Step 9: Create Admin User

```bash
# Create admin user via API
curl -X POST http://localhost:8000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"admin\", \"email\": \"admin@example.com\", \"password\": \"admin123\", \"is_admin\": true}"
```

**Expected Output:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_active": true,
  "is_admin": true,
  "created_at": "2024-..."
}
```

## Step 10: Access Dashboard

Open in browser:
```
http://localhost:3000
```

You should see the login page.

## Step 11: Login to Dashboard

1. Enter username: `admin`
2. Enter password: `admin123`
3. Click "Sign in"

You should be redirected to the main dashboard.

## Step 12: Explore Dashboard Features

### View Dashboard Stats
- Click "Dashboard" in sidebar
- You'll see statistics (may be empty initially)

### Create a Firewall Rule
1. Click "Rules" in sidebar
2. Click "+ New Rule"
3. Fill in:
   - Name: "Block Example Domain"
   - Scope: Global
   - Action: Deny
   - Domain: example.com
4. Click "Create Rule"

### View Devices
- Click "Devices" in sidebar
- See registered devices (empty until agents connect)

### View Alerts
- Click "Alerts" in sidebar
- See anomaly alerts (empty until anomalies detected)

## Step 13: Test API Endpoints

### Get All Rules
```bash
# First, get a token by logging in
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=admin&password=admin123"
```

Copy the `access_token` from the response, then:

```bash
# Replace YOUR_TOKEN with the actual token
curl http://localhost:8000/api/v1/rules ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Step 14: Monitor Real-Time Activity

### Watch Backend Logs
```bash
docker-compose logs -f backend
```

### Watch Celery Worker Logs
```bash
docker-compose logs -f celery
```

### Watch Dashboard Logs
```bash
docker-compose logs -f dashboard
```

## Step 15: Test WebSocket Connection

The dashboard automatically connects to WebSocket for real-time alerts. You can verify this by:

1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Filter by "WS" (WebSocket)
4. You should see a connection to `ws://localhost:8000/ws/alerts`

## Expected Output Summary

### ✅ Successful Startup Indicators:

1. **Docker Services**: All services show "Up" status
2. **Backend Health**: `http://localhost:8000/health` returns `{"status": "healthy"}`
3. **API Docs**: `http://localhost:8000/docs` shows Swagger UI
4. **Dashboard**: `http://localhost:3000` shows login page
5. **Database**: PostgreSQL is accepting connections
6. **Redis**: Redis is running
7. **Celery**: Worker is processing tasks

### 📊 What You Should See:

- **Dashboard**: Modern UI with sidebar navigation
- **API Docs**: Interactive Swagger interface
- **Logs**: Services starting up without errors
- **Database**: Tables created automatically on first run

## Troubleshooting

### If Services Won't Start:

```bash
# Check what's wrong
docker-compose ps
docker-compose logs

# Restart services
docker-compose down
docker-compose up -d
```

### If Port is Already in Use:

```bash
# Find what's using the port (Windows)
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Stop the conflicting service or change ports in docker-compose.yml
```

### If Database Connection Fails:

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### If Dashboard Won't Load:

```bash
# Check dashboard logs
docker-compose logs dashboard

# Rebuild dashboard
docker-compose up -d --build dashboard
```

## Stopping the Project

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Next Steps After Running

1. **Create Rules**: Add firewall rules via dashboard
2. **Deploy Agents**: Set up Windows/Linux agents (see AGENT_SETUP.md)
3. **Monitor Activity**: Watch for telemetry and alerts
4. **Test Anomaly Detection**: Generate traffic to trigger ML analysis

## Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:3000 | Web UI |
| API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health | http://localhost:8000/health | Health check |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Task queue |

---

**You're all set!** The project should now be running and accessible.



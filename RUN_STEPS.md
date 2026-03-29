# 🚀 Step-by-Step: Run NeuroWall Project

## Option 1: Using Docker (Recommended - Easiest)

### Prerequisites
- Install Docker Desktop for Windows: https://www.docker.com/products/docker-desktop
- After installation, restart your computer
- Make sure Docker Desktop is running (check system tray)

### Step-by-Step with Docker

#### Step 1: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop
2. Install and restart your computer
3. Start Docker Desktop
4. Wait for Docker to fully start (whale icon in system tray)

#### Step 2: Open Command Prompt in Project Directory
```cmd
cd D:\neurowall
```

#### Step 3: Start All Services
```cmd
docker-compose up -d
```

**First time will take 2-5 minutes** (downloading images and building)

#### Step 4: Check Services are Running
```cmd
docker-compose ps
```

Wait until all services show "Up" (about 30-60 seconds)

#### Step 5: Access the Dashboard
Open browser: **http://localhost:3000**

#### Step 6: Create Admin User
Open new Command Prompt and run:
```cmd
curl -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"email\": \"admin@example.com\", \"password\": \"admin123\", \"is_admin\": true}"
```

Or use PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

#### Step 7: Login to Dashboard
1. Go to: http://localhost:3000
2. Username: `admin`
3. Password: `admin123`
4. Click "Sign in"

#### Step 8: Explore!
- **Dashboard**: View statistics
- **Rules**: Create firewall rules
- **Devices**: See connected devices
- **Alerts**: View anomaly alerts

---

## Option 2: Manual Setup (Without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis
- Node.js 20+

### Step 1: Setup Backend

```cmd
cd D:\neurowall\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your database settings

# Start backend
python run.py
```

Backend will run on: **http://localhost:8000**

### Step 2: Setup Celery Worker (New Terminal)

```cmd
cd D:\neurowall\backend
venv\Scripts\activate
celery -A app.celery_app worker --loglevel=info
```

### Step 3: Setup Dashboard (New Terminal)

```cmd
cd D:\neurowall\dashboard

# Install dependencies
npm install

# Start dashboard
npm run dev
```

Dashboard will run on: **http://localhost:3000**

### Step 4: Create Admin User

Open browser: http://localhost:8000/docs

Use the Swagger UI to:
1. POST `/api/v1/auth/register`
2. Body:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123",
  "is_admin": true
}
```

### Step 5: Login to Dashboard

Go to: http://localhost:3000
- Username: `admin`
- Password: `admin123`

---

## Quick Verification Checklist

### ✅ Check Backend is Running
Open: http://localhost:8000/health
Should see: `{"status": "healthy"}`

### ✅ Check API Documentation
Open: http://localhost:8000/docs
Should see: Swagger UI with all endpoints

### ✅ Check Dashboard
Open: http://localhost:3000
Should see: Login page

### ✅ Check Database
Backend should create tables automatically on first run

---

## What You'll See When Running

### Terminal Output (Docker):
```
Creating network "neurowall_default" ...
Creating neurowall_postgres_1 ... done
Creating neurowall_redis_1 ... done
Creating neurowall_backend_1 ... done
Creating neurowall_celery_1 ... done
Creating neurowall_dashboard_1 ... done
```

### Backend Logs:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Dashboard:
- Modern UI with sidebar
- Login page initially
- Main dashboard after login

---

## Common Issues & Solutions

### Issue: "docker is not recognized"
**Solution**: Install Docker Desktop and restart computer

### Issue: Port 8000 already in use
**Solution**: 
```cmd
# Find what's using the port
netstat -ano | findstr :8000
# Kill the process or change port in docker-compose.yml
```

### Issue: Can't connect to database
**Solution**: 
- Check PostgreSQL is running (Docker: `docker-compose ps postgres`)
- Verify DATABASE_URL in .env file

### Issue: Dashboard shows errors
**Solution**:
```cmd
# Check logs
docker-compose logs dashboard
# Or for manual setup: Check browser console (F12)
```

---

## Viewing Logs

### Docker:
```cmd
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
docker-compose logs -f celery
```

### Manual Setup:
- Backend: Check terminal running `python run.py`
- Celery: Check terminal running celery worker
- Dashboard: Check terminal running `npm run dev`

---

## Stopping the Project

### Docker:
```cmd
docker-compose down
```

### Manual:
- Press `Ctrl+C` in each terminal window
- Stop PostgreSQL and Redis manually

---

## Next Steps After Running

1. ✅ **Create Rules**: Dashboard → Rules → + New Rule
2. ✅ **View API Docs**: http://localhost:8000/docs
3. ✅ **Test Endpoints**: Use Swagger UI to test APIs
4. ✅ **Monitor Logs**: Watch for telemetry and alerts
5. ✅ **Deploy Agents**: See AGENT_SETUP.md for agent deployment

---

## Quick Commands Reference

| Action | Docker Command | Manual Command |
|--------|---------------|----------------|
| Start | `docker-compose up -d` | See manual steps above |
| Stop | `docker-compose down` | `Ctrl+C` in terminals |
| Logs | `docker-compose logs -f` | Check terminal windows |
| Status | `docker-compose ps` | Check processes |
| Restart | `docker-compose restart` | Stop and start again |

---

## Expected URLs

| Service | URL | Status Check |
|---------|-----|--------------|
| Dashboard | http://localhost:3000 | Login page |
| API | http://localhost:8000 | Health endpoint |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health | http://localhost:8000/health | `{"status": "healthy"}` |

---

**🎉 You're ready to run!** Choose Option 1 (Docker) for easiest setup, or Option 2 (Manual) if you prefer more control.



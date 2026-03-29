# 🐳 How to Run NeuroWall in Docker

## Step-by-Step Instructions

### Step 1: Navigate to Project Directory
```cmd
cd D:\neurowall
```

### Step 2: Start All Services
```cmd
docker-compose up -d --build
```

**What this does:**
- Builds all Docker images (first time: 5-10 minutes)
- Starts all services in background
- Downloads dependencies automatically

**First time will take longer** - be patient! ⏳

### Step 3: Wait for Services to Start
```cmd
docker-compose ps
```

Wait until all services show **"Up"** status (about 30-60 seconds after build completes)

You should see:
```
NAME                    STATUS
neurowall_postgres_1    Up
neurowall_redis_1       Up
neurowall_backend_1     Up
neurowall_celery_1      Up
neurowall_dashboard_1   Up
```

### Step 4: Verify Backend is Running
Open browser: **http://localhost:8000/health**

Should see: `{"status": "healthy"}`

### Step 5: Create Admin User

**Option A - PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

**Option B - Browser (Swagger UI):**
1. Go to: **http://localhost:8000/docs**
2. Find `POST /api/v1/auth/register`
3. Click **"Try it out"**
4. Paste this JSON:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123",
  "is_admin": true
}
```
5. Click **"Execute"**

### Step 6: Login to Dashboard
Open: **http://localhost:3000**

Login with:
- Username: `admin`
- Password: `admin123`

---

## ✅ You're Done!

The NeuroWall dashboard should now be running! 🎉

---

## Daily Commands

### Start Project
```cmd
docker-compose up -d
```

### Stop Project
```cmd
docker-compose down
```

### View Logs
```cmd
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
```

### Check Status
```cmd
docker-compose ps
```

### Restart Services
```cmd
docker-compose restart
```

---

## Access Points

| Service | URL | What It Is |
|---------|-----|------------|
| **Dashboard** | http://localhost:3000 | Main web interface |
| **API** | http://localhost:8000 | Backend API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health** | http://localhost:8000/health | Health check |

---

## Troubleshooting

### Services Won't Start
```cmd
# Check what's wrong
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d --build
```

### Port Already in Use
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000

# Or change ports in docker-compose.yml
```

### Build Fails
```cmd
# Clean and rebuild
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### View Real-Time Logs
```cmd
docker-compose logs -f
```
Press `Ctrl+C` to exit

---

## Quick Reference

```cmd
# Start everything
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

---

**That's it!** Just run `docker-compose up -d --build` and wait for it to complete! 🚀


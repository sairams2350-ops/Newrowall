# 🐳 Complete Docker Setup Guide for NeuroWall

## Why Docker?
- ✅ No manual dependency installation
- ✅ Everything runs in containers
- ✅ One command to start everything
- ✅ Works the same on any computer
- ✅ No Python version conflicts

---

## Step 1: Install Docker Desktop

### Download Docker Desktop
1. Go to: **https://www.docker.com/products/docker-desktop/**
2. Click **"Download for Windows"**
3. Run the installer: `Docker Desktop Installer.exe`

### Installation Steps
1. **Run the installer**
   - Check "Use WSL 2 instead of Hyper-V" (recommended)
   - Click "Ok" to install

2. **Restart your computer** when prompted
   - This is required!

3. **Start Docker Desktop**
   - Look for Docker icon in system tray (whale icon)
   - Wait for it to fully start (icon stops animating)
   - First time may take 2-3 minutes

4. **Verify Docker is running**
   - Open Command Prompt
   - Run: `docker --version`
   - Should show: `Docker version 24.x.x` or similar

### Enable WSL 2 (If Needed)
If Docker asks for WSL 2:
1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart computer
4. Start Docker Desktop again

---

## Step 2: Verify Docker is Working

Open Command Prompt and test:

```cmd
docker --version
docker-compose --version
```

Both should show version numbers.

---

## Step 3: Setup NeuroWall with Docker

### Navigate to Project
```cmd
cd D:\neurowall
```

### Start Everything (One Command!)
```cmd
docker-compose up -d
```

**First time will:**
- Download images (2-5 minutes)
- Build containers
- Start all services

**You'll see:**
```
Creating network "neurowall_default" ...
Creating neurowall_postgres_1 ...
Creating neurowall_redis_1 ...
Creating neurowall_backend_1 ...
Creating neurowall_celery_1 ...
Creating neurowall_dashboard_1 ...
```

### Wait for Services to Start
```cmd
docker-compose ps
```

Wait until all services show **"Up"** status (about 30-60 seconds).

---

## Step 4: Create Admin User

Open PowerShell and run:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

Or use browser:
1. Go to: http://localhost:8000/docs
2. Find `POST /api/v1/auth/register`
3. Click "Try it out"
4. Paste this JSON:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123",
  "is_admin": true
}
```
5. Click "Execute"

---

## Step 5: Access the Dashboard

Open browser: **http://localhost:3000**

Login with:
- Username: `admin`
- Password: `admin123`

**Done!** 🎉

---

## Daily Usage Commands

### Start Project
```cmd
cd D:\neurowall
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

### Rebuild (if code changes)
```cmd
docker-compose up -d --build
```

---

## Troubleshooting

### Docker Desktop Won't Start
1. Make sure virtualization is enabled in BIOS
2. Check Windows features: Enable "Virtual Machine Platform" and "Windows Subsystem for Linux"
3. Restart computer

### Port Already in Use
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Services Won't Start
```cmd
# Check logs
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d
```

### Out of Disk Space
```cmd
# Clean up Docker
docker system prune -a
```

### Reset Everything
```cmd
# Stop and remove everything (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

---

## What's Running in Docker

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Task queue |
| Backend API | 8000 | FastAPI server |
| Celery Worker | - | ML processing |
| Dashboard | 3000 | Next.js UI |

---

## Benefits of Docker Setup

✅ **No Python installation needed**  
✅ **No pip install issues**  
✅ **No version conflicts**  
✅ **Consistent environment**  
✅ **Easy to start/stop**  
✅ **Isolated from your system**  

---

## Quick Reference

```cmd
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Status
docker-compose ps

# Restart
docker-compose restart
```

---

## Access Points

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

**That's it!** Once Docker is installed, you'll never have to worry about dependencies again. Just run `docker-compose up -d` and everything works! 🚀


# ⚡ Docker Quick Start - 3 Steps

## Step 1: Install Docker Desktop (5 minutes)

1. **Download**: https://www.docker.com/products/docker-desktop/
2. **Install**: Run the installer
3. **Restart**: Your computer (required!)
4. **Start**: Docker Desktop (wait for whale icon in system tray)

## Step 2: Start Project (1 command)

```cmd
cd D:\neurowall
docker-compose up -d
```

Wait 2-3 minutes (first time downloads images)

## Step 3: Create Admin & Login

**Create admin** (PowerShell):
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

**Login**: http://localhost:3000
- Username: `admin`
- Password: `admin123`

---

## Daily Commands

```cmd
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

**That's it!** No more manual setup! 🎉


# 🚀 START HERE - Docker Setup (Easiest Way!)

## ⚡ Super Quick Setup (3 Steps)

### 1️⃣ Install Docker Desktop
- Download: **https://www.docker.com/products/docker-desktop/**
- Install it
- **Restart your computer** (important!)
- Start Docker Desktop (wait for whale icon 🐳)

### 2️⃣ Start Project
```cmd
cd D:\neurowall
docker-compose up -d
```
Wait 2-3 minutes (first time only)

### 3️⃣ Create Admin & Login
**Create admin** (PowerShell):
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

**Login**: http://localhost:3000
- Username: `admin`
- Password: `admin123`

---

## ✅ That's It! You're Done!

No more:
- ❌ Installing Python
- ❌ Installing pip packages
- ❌ Dealing with version conflicts
- ❌ Manual setup

Just:
- ✅ `docker-compose up -d` to start
- ✅ `docker-compose down` to stop

---

## 📚 Need More Details?

- **Full guide**: See `DOCKER_SETUP_COMPLETE.md`
- **Quick reference**: See `DOCKER_QUICK_START.md`

---

**Enjoy your automated setup!** 🎉



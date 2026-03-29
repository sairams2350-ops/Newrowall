# 🚀 Run NeuroWall Now - Step by Step

## ✅ Docker is Installed!

Now let's start the project:

---

## Step 1: Start All Services

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

---

## Step 2: Wait for Services to Start

```cmd
docker-compose ps
```

Wait until all services show **"Up"** (about 30-60 seconds)

---

## Step 3: Verify Backend is Running

Open browser: **http://localhost:8000/health**

Should see: `{"status": "healthy"}`

---

## Step 4: Create Admin User

**Option A - PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

**Option B - Browser (Swagger UI):**
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

## Step 5: Login to Dashboard

Open: **http://localhost:3000**

Login:
- Username: `admin`
- Password: `admin123`

---

## ✅ You're Done!

You should now see the NeuroWall dashboard! 🎉

---

## Useful Commands

```cmd
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Check status
docker-compose ps
```

---

## Access Points

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health


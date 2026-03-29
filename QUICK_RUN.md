# ⚡ Quick Run Guide - NeuroWall

## 🎯 Fastest Way to Run (Docker)

### 1. Install Docker Desktop
Download: https://www.docker.com/products/docker-desktop
- Install and restart computer
- Start Docker Desktop

### 2. Run These Commands

```cmd
cd D:\neurowall
docker-compose up -d
```

Wait 1-2 minutes for services to start.

### 3. Open in Browser

**Dashboard**: http://localhost:3000  
**API Docs**: http://localhost:8000/docs

### 4. Create Admin User

**Option A - Using PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -ContentType "application/json" -Body '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
```

**Option B - Using Browser:**
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

### 5. Login

Go to: http://localhost:3000
- Username: `admin`
- Password: `admin123`

### 6. Done! 🎉

You should now see the NeuroWall dashboard!

---

## 🔍 Verify It's Working

### Check Health:
http://localhost:8000/health → Should show `{"status": "healthy"}`

### Check Services:
```cmd
docker-compose ps
```
All should show "Up"

### Check Logs:
```cmd
docker-compose logs -f
```
Press `Ctrl+C` to exit

---

## 🛑 Stop the Project

```cmd
docker-compose down
```

---

## ❌ Troubleshooting

**Docker not found?**
- Install Docker Desktop first
- Restart computer after installation

**Port already in use?**
- Close other applications using ports 3000, 8000
- Or change ports in `docker-compose.yml`

**Services won't start?**
```cmd
docker-compose down
docker-compose up -d
```

**Need more help?**
- See `RUN_STEPS.md` for detailed instructions
- See `README.md` for full documentation

---

**That's it!** The project should be running now. 🚀



# NeuroWall: AI-Driven Per-Application Firewall

NeuroWall is a production-ready, AI-driven per-application firewall system for endpoint security. It provides kernel-level packet filtering with real-time anomaly detection using rolling Z-score statistical analysis.

## 🏗️ Architecture

```
┌─────────────────┐
│   Dashboard     │  Next.js + Tailwind
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP/WebSocket
         │
┌────────▼────────┐
│   Backend API   │  FastAPI + PostgreSQL
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │        │
┌───▼───┐ ┌──▼────┐
│ Redis │ │ Celery│  Background ML Processing
└───────┘ └───────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌───▼───┐
│ Agent │ │ Agent │  Rust Agents (Windows/Linux)
│Windows│ │ Linux │  WFP / eBPF
└───────┘ └───────┘
```

## 📋 Features

### Core Functionality
- **Per-Application Firewall**: Kernel-level filtering based on process identification
- **Real-Time Anomaly Detection**: Rolling Z-score statistical model
- **Centralized Rule Management**: Global, device, and application-level rules
- **Policy Signing & Verification**: HMAC-based policy integrity
- **Telemetry Collection**: Comprehensive flow logging
- **WebSocket Alerts**: Real-time anomaly notifications

### Performance Requirements
- **<5% CPU Overhead**: Optimized agent implementation
- **<3ms Latency**: Kernel-level filtering
- **Streaming Logs**: Efficient telemetry batching

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Rust 1.70+ (for agent development)
- Node.js 20+ (for dashboard development)

### Using Docker Compose (Recommended)

**This is the easiest way to run the full demo (Backend + Dashboard + AI Simulator).**

1. **Start all services:**
   ```bash
   docker-compose up -d --build
   ```

2. **Access the Dashboard:**
   - Open [http://localhost:3000](http://localhost:3000)
   - Login with default credentials:
     - **Username:** `admin`
     - **Password:** `admin123`

> **Note:** The `simulator` container will automatically start generating traffic and simulated attacks. You do NOT need to run any extra scripts.

### Checking Logs
To see the simulated traffic in real-time in your terminal:
```bash
docker-compose logs -f simulator
```

### Manual Setup

#### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (if using Alembic)
# alembic upgrade head

# Start backend
python run.py
```

#### 2. Celery Worker (ML Processing)

```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

#### 3. Dashboard Setup

```bash
cd dashboard
npm install
npm run dev
```

#### 4. Agent Setup

**Windows Agent:**
```bash
cd agent/windows
cargo build --release
# Run as administrator
sudo ./target/release/neurowall-agent-windows
```

**Linux Agent:**
```bash
cd agent/linux
cargo build --release
# Run with appropriate permissions
sudo ./target/release/neurowall-agent-linux
```

## 📚 System Components

### Backend API

**Technology Stack:**
- FastAPI (Python)
- PostgreSQL with SQLAlchemy ORM
- Redis for Celery task queue
- WebSockets for real-time alerts
- JWT authentication

**Key Endpoints:**
- `/api/v1/auth/*` - Authentication
- `/api/v1/rules/*` - Firewall rule management
- `/api/v1/devices/*` - Device management
- `/api/v1/telemetry/*` - Telemetry collection
- `/api/v1/alerts/*` - Alert management
- `/api/v1/policies/*` - Policy generation and deployment
- `/ws/alerts` - WebSocket for real-time alerts

### ML Engine

**Anomaly Detection Algorithm:**
- **Rolling Z-Score**: Statistical anomaly detection
- **Window Size**: 1000 samples (configurable)
- **Thresholds**: 
  - Low: |z| ≥ 2.0
  - Medium: |z| ≥ 2.5
  - High: |z| ≥ 3.0
  - Critical: |z| ≥ 3.0

**Mathematical Model:**
```
Rolling Mean:    μ_t = (1/n) * Σ(x_i)
Rolling Variance: σ²_t = (1/n) * Σ(x_i - μ_t)²
Rolling Std Dev:  σ_t = √σ²_t
Z-Score:         z = (x - μ_t) / σ_t
```

**Features Extracted:**
- Bytes sent/received
- Total bytes
- Destination port
- Connection patterns

### Agents

**Windows Agent:**
- Uses Windows Filtering Platform (WFP)
- Kernel-level packet interception
- Process identification via PID
- Local policy cache (JSON)

**Linux Agent:**
- Uses eBPF for packet filtering
- Netlink for connection monitoring
- Process identification via PID
- Local policy cache (JSON)

**Communication:**
- gRPC secure channel
- Policy updates via heartbeat
- Telemetry batching (100 entries or 5s interval)

### Dashboard

**Features:**
- Real-time WebSocket alert feed
- Rule management UI
- Device status monitoring
- Telemetry statistics and charts
- Policy deployment status

## 🔐 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Admin and user roles

### Policy Security
- HMAC-SHA256 policy signing
- Signature verification on agents
- Secure gRPC communication (TLS-ready)

### Agent Security
- Mutual authentication
- Policy integrity verification
- Secure telemetry transmission

## 📖 API Documentation

Full API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

**Register Device:**
```bash
curl -X POST http://localhost:8000/api/v1/devices \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "device_id": "device-123",
    "hostname": "workstation-01",
    "platform": "windows"
  }'
```

**Create Rule:**
```bash
curl -X POST http://localhost:8000/api/v1/rules \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Block Malicious IP",
    "scope": "global",
    "action": "deny",
    "destination_ip": "192.168.1.100",
    "priority": 10
  }'
```

**Get Alerts:**
```bash
curl http://localhost:8000/api/v1/alerts \
  -H "Authorization: Bearer <token>"
```

## 🔄 How It Works

### End-to-End Flow

1. **Agent Registration**
   - Agent starts and registers with backend via gRPC
   - Backend creates device record
   - Agent receives initial policy

2. **Policy Application**
   - Agent caches policy locally (JSON)
   - Kernel-level filter engine applies rules
   - Each connection attempt is evaluated against rules

3. **Telemetry Collection**
   - Agent collects flow information:
     - Process ID and name
     - Destination IP/port/domain
     - Protocol
     - Bytes sent/received
     - Action taken (allow/deny)
   - Telemetry batched and sent to backend

4. **Anomaly Detection**
   - Backend receives telemetry
   - Celery task processes log asynchronously
   - ML engine calculates Z-score against baseline
   - If anomaly detected, alert created and broadcast via WebSocket

5. **Real-Time Alerts**
   - Dashboard connects to WebSocket
   - Alerts pushed in real-time
   - Users can acknowledge alerts

### Rule Evaluation

Rules are evaluated in priority order (lower number = higher priority):
1. Application-specific rules
2. Device-specific rules
3. Global rules
4. Default deny (if no rule matches)

### Policy Updates

1. Admin creates/updates rule in dashboard
2. Policy regenerated for affected devices
3. Policy signed with HMAC
4. Agent receives policy update on next heartbeat
5. Agent verifies signature and updates local cache
6. New rules apply immediately

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Agent Tests
```bash
cd agent/windows  # or agent/linux
cargo test
```

## 📝 Configuration

### Backend Configuration (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/neurowall
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379/0
ML_WINDOW_SIZE=1000
ML_Z_SCORE_THRESHOLD=2.5
```

### Agent Configuration (config.json)
```json
{
  "device_id": "auto-generated-uuid",
  "server_url": "http://localhost:8000",
  "grpc_endpoint": "http://localhost:50051",
  "heartbeat_interval_secs": 30,
  "telemetry_batch_size": 100,
  "telemetry_flush_interval_secs": 5
}
```

## 🐛 Troubleshooting

### Agent Not Connecting
- Check firewall rules
- Verify gRPC endpoint is accessible
- Check agent logs for errors
- Ensure agent has proper permissions (admin/root)

### No Alerts Appearing
- Verify Celery worker is running
- Check Redis connection
- Verify ML processing tasks are executing
- Check backend logs for errors

### Dashboard Not Loading
- Verify API_URL environment variable
- Check CORS settings in backend
- Verify authentication token

## 📄 License

[Specify your license here]

## 🤝 Contributing

[Contributing guidelines]

## 📧 Contact

[Contact information]

---

**NeuroWall** - AI-Driven Per-Application Firewall for Endpoint Security


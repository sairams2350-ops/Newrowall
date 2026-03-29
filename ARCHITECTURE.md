# NeuroWall Architecture Documentation

## System Overview

NeuroWall is a distributed firewall system with the following key components:

1. **Backend API** - Central management and processing
2. **ML Engine** - Anomaly detection using rolling Z-score
3. **Agents** - Kernel-level filtering on endpoints
4. **Dashboard** - Web-based management interface

## Component Details

### Backend API

**Technology:**
- FastAPI (Python 3.11+)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Redis (task queue)
- Celery (background workers)
- WebSockets (real-time alerts)

**Responsibilities:**
- User authentication and authorization
- Rule management (CRUD operations)
- Device registration and tracking
- Policy generation and signing
- Telemetry collection and storage
- Alert generation and broadcasting
- ML task orchestration

**Key Modules:**
- `app/models.py` - Database models
- `app/routers/` - API endpoints
- `app/auth.py` - Authentication logic
- `app/tasks.py` - Celery tasks
- `app/websocket.py` - WebSocket manager

### ML Engine

**Location:** `ml/anomaly_detector.py`

**Algorithm: Rolling Z-Score**

The anomaly detection uses a rolling statistical window to establish baselines and detect deviations.

**Mathematical Foundation:**

1. **Rolling Mean (μ_t):**
   ```
   μ_t = (1/n) * Σ(x_i) for i in [t-n+1, t]
   ```
   Where n is the window size (default: 1000)

2. **Rolling Variance (σ²_t):**
   ```
   σ²_t = (1/n) * Σ(x_i - μ_t)²
   ```

3. **Rolling Standard Deviation (σ_t):**
   ```
   σ_t = √σ²_t
   ```

4. **Z-Score Calculation:**
   ```
   z = (x - μ_t) / σ_t
   ```

**Feature Extraction:**
- `bytes_sent`: Bytes transmitted
- `bytes_received`: Bytes received
- `total_bytes`: Sum of sent and received
- `destination_port`: Target port number

**Baseline Management:**
- Per-device baselines maintained in memory
- Rolling window of recent telemetry logs
- Automatic baseline updates with new data

**Anomaly Thresholds:**
- **Low**: |z| ≥ 2.0
- **Medium**: |z| ≥ 2.5
- **High**: |z| ≥ 2.5
- **Critical**: |z| ≥ 3.0

### Agents

**Technology:**
- Rust (for performance and safety)
- gRPC (secure communication)
- Platform-specific APIs:
  - Windows: Windows Filtering Platform (WFP)
  - Linux: eBPF + Netlink

**Architecture:**

```
Agent
├── Policy Cache (JSON)
│   └── Rules sorted by priority
├── Filter Engine
│   ├── Windows: WFP callouts
│   └── Linux: eBPF programs
├── Telemetry Collector
│   └── Batches and sends to backend
└── gRPC Client
    ├── Policy Service
    └── Telemetry Service
```

**Process Flow:**

1. **Initialization:**
   - Load configuration
   - Register with backend
   - Fetch initial policy
   - Initialize filter engine

2. **Packet Processing:**
   - Kernel intercepts packet
   - Extract process information (PID)
   - Match against policy rules
   - Allow or deny connection
   - Collect telemetry

3. **Telemetry Collection:**
   - Buffer telemetry entries
   - Batch when buffer full or timeout
   - Send to backend via gRPC

4. **Policy Updates:**
   - Heartbeat every 30 seconds
   - Check for policy updates
   - Verify signature
   - Update local cache
   - Apply new rules

**Rule Evaluation:**

Rules are evaluated in priority order:
1. Check application-specific rules
2. Check device-specific rules
3. Check global rules
4. Default: DENY

**Performance Targets:**
- <5% CPU overhead
- <3ms latency per decision
- Efficient memory usage

### Dashboard

**Technology:**
- Next.js 14 (React framework)
- Tailwind CSS (styling)
- Recharts (data visualization)
- WebSocket client (real-time updates)

**Features:**
- **Stats View**: Overview of traffic and anomalies
- **Rules View**: Create, edit, delete firewall rules
- **Devices View**: Monitor connected endpoints
- **Alerts View**: Real-time anomaly alerts

**Real-Time Updates:**
- WebSocket connection to backend
- Automatic alert notifications
- Live device status updates

## Data Flow

### Telemetry Flow

```
Agent → gRPC → Backend API → Database
                          ↓
                    Celery Task Queue
                          ↓
                    ML Engine (Z-Score)
                          ↓
                    Alert Generation
                          ↓
                    WebSocket Broadcast
                          ↓
                    Dashboard (Real-time)
```

### Policy Flow

```
Dashboard → Backend API → Policy Generation
                              ↓
                         Policy Signing (HMAC)
                              ↓
                         Database Storage
                              ↓
                    Agent Heartbeat Request
                              ↓
                         Policy Delivery (gRPC)
                              ↓
                    Agent Signature Verification
                              ↓
                         Local Cache Update
                              ↓
                         Kernel Filter Update
```

## Security Architecture

### Authentication

1. **User Authentication:**
   - Username/password login
   - JWT token generation
   - Token validation on each request

2. **Agent Authentication:**
   - Device registration
   - gRPC mutual TLS (ready)
   - Policy signature verification

### Policy Security

1. **Policy Signing:**
   - HMAC-SHA256 signature
   - Secret key stored server-side
   - Signature included in policy

2. **Policy Verification:**
   - Agent verifies signature on receipt
   - Rejects invalid policies
   - Logs security events

### Communication Security

- TLS for HTTP/HTTPS (production)
- gRPC with TLS (production)
- WebSocket over WSS (production)

## Database Schema

### Core Tables

- **users**: User accounts and roles
- **devices**: Registered endpoints
- **applications**: Known applications
- **rules**: Firewall rules
- **policies**: Signed policies
- **telemetry_logs**: Flow data
- **alerts**: Anomaly alerts

### Relationships

```
User → Rules (created_by)
Device → Rules (device_id)
Device → Policies (device_id)
Device → TelemetryLogs (device_id)
Device → Alerts (device_id)
Application → Rules (application_id)
Rule → Policies (rule_id)
TelemetryLog → Alert (telemetry_log_id)
```

## Deployment Architecture

### Development

```
┌─────────────┐
│  Dashboard  │  localhost:3000
└──────┬──────┘
       │
┌──────▼──────┐
│   Backend   │  localhost:8000
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│Redis│ │Postgres│
└─────┘ └──────┘
```

### Production

Recommended production architecture:
- Load balancer (nginx/traefik)
- Backend API (multiple instances)
- PostgreSQL (primary + replicas)
- Redis cluster
- Celery workers (scalable)
- Dashboard (CDN + caching)

## Performance Considerations

### Backend
- Database connection pooling
- Redis caching for policies
- Async request handling
- Celery task batching

### Agents
- Kernel-level filtering (minimal overhead)
- Efficient rule matching (priority-sorted)
- Telemetry batching (reduces network calls)
- Local policy cache (fast lookups)

### ML Engine
- In-memory baseline storage
- Efficient statistical calculations
- Per-device isolation
- Configurable window sizes

## Monitoring & Observability

### Metrics to Monitor
- Agent CPU usage
- Network latency
- Policy update frequency
- Anomaly detection rate
- Alert acknowledgment rate
- Telemetry processing time

### Logging
- Structured logging (JSON)
- Log levels: DEBUG, INFO, WARN, ERROR
- Centralized log aggregation (recommended)

## Scalability

### Horizontal Scaling
- Backend API: Stateless, can scale horizontally
- Celery workers: Can add more workers
- Agents: One per endpoint (natural scaling)

### Vertical Scaling
- Database: Increase resources for larger datasets
- Redis: Increase memory for larger queues

## Future Enhancements

1. **Advanced ML Models:**
   - Deep learning for pattern recognition
   - Ensemble methods
   - Adaptive thresholds

2. **Enhanced Features:**
   - Application fingerprinting
   - Behavioral analysis
   - Threat intelligence integration

3. **Performance:**
   - eBPF optimization
   - Zero-copy packet processing
   - Hardware acceleration

---

**Document Version:** 1.0  
**Last Updated:** 2024


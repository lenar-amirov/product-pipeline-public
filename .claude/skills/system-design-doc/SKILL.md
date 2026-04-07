---
name: system-design-doc
description: Creates system design documents covering architecture, technical dependencies, data flows, APIs, and infrastructure. Use when user needs to document technical architecture, identify dependencies, or says "system design", "architecture document", "technical dependencies", "design doc", "системный дизайн", "архитектурный документ".
---
# System Design Document Specialist

You are an expert in creating comprehensive system design documents for software engineering projects. You understand how to translate complex technical requirements into clear, actionable design specifications that serve as blueprints for development teams, stakeholders, and future maintainers.

## Core Document Structure

Every system design document should follow this hierarchical structure:

1. **Executive Summary** - High-level overview for stakeholders
2. **Requirements Analysis** - Functional and non-functional requirements
3. **System Architecture** - High-level system components and interactions
4. **Detailed Design** - Component specifications, APIs, data models
5. **Implementation Plan** - Phases, timelines, dependencies
6. **Operational Considerations** - Monitoring, scaling, maintenance
7. **Risk Assessment** - Technical risks and mitigation strategies

## Architecture Documentation Standards

### Component Diagrams
Use C4 model hierarchy for architectural representation:

```mermaid
graph TB
    User[User] --> LB[Load Balancer]
    LB --> API1[API Server 1]
    LB --> API2[API Server 2]
    API1 --> Cache[Redis Cache]
    API2 --> Cache
    API1 --> DB[(Primary Database)]
    API2 --> DB
    DB --> Replica[(Read Replica)]
```

### API Specifications
Document all interfaces with OpenAPI-style specifications:

```yaml
endpoints:
  /api/v1/users:
    POST:
      summary: Create new user
      request_body:
        required: [email, password]
        properties:
          email: {type: string, format: email}
          password: {type: string, minLength: 8}
      responses:
        201: {description: User created successfully}
        400: {description: Invalid input data}
```

## Non-Functional Requirements Framework

### Performance Specifications
Quantify all performance requirements with specific metrics:

- **Throughput**: "System must handle 10,000 requests/second at peak load"
- **Latency**: "API responses must complete within 200ms for 95th percentile"
- **Availability**: "99.9% uptime (8.77 hours downtime/year maximum)"
- **Scalability**: "Must scale horizontally to support 10x traffic growth"

### Data Volume Projections
```
Daily Active Users: 100,000
Average Requests per User: 50
Daily Request Volume: 5,000,000
Data Growth Rate: 20% monthly
Storage Requirements: 500GB initial, 2TB projected year 1
```

## Database Design Documentation

### Schema Definitions
Include complete table structures with constraints:

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    status user_status_enum DEFAULT 'active',
    INDEX idx_email (email),
    INDEX idx_status_created (status, created_at)
);

CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Data Flow Diagrams
Document how data moves through the system:

```
Client Request → API Gateway → Authentication Service → Business Logic → Database
                    ↓              ↓                    ↓             ↓
                 Rate Limiting   JWT Validation     Cache Layer   Connection Pool
```

## Scalability and Performance Patterns

### Caching Strategy
```
L1 Cache: Application memory (Redis) - 1ms latency
L2 Cache: Distributed cache (Redis Cluster) - 5ms latency
L3 Cache: CDN (CloudFront) - 50ms latency

Cache Invalidation:
- Time-based: User sessions (30 minutes)
- Event-based: User profile updates
- Manual: Configuration changes
```

### Load Balancing Configuration
```nginx
upstream api_servers {
    least_conn;
    server api1.internal:8080 max_fails=3 fail_timeout=30s;
    server api2.internal:8080 max_fails=3 fail_timeout=30s;
    server api3.internal:8080 max_fails=3 fail_timeout=30s;
}

server {
    location /api/ {
        proxy_pass http://api_servers;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
    }
}
```

## Security Architecture

### Authentication Flow
```
1. User submits credentials
2. System validates against user store
3. JWT token generated with 15-minute expiry
4. Refresh token stored (7-day expiry)
5. All API requests include JWT in Authorization header
6. Token validation middleware checks signature and expiry
```

### Data Protection Measures
- **Encryption at Rest**: AES-256 for sensitive data fields
- **Encryption in Transit**: TLS 1.3 for all communications
- **Access Control**: RBAC with principle of least privilege
- **Audit Logging**: All data access and modifications logged

## Deployment and Operations

### Environment Configuration
```yaml
production:
  database:
    host: prod-db-cluster.internal
    connection_pool: 50
    read_replicas: 2
  cache:
    redis_cluster: prod-redis.internal:6379
    max_connections: 100
  monitoring:
    metrics_endpoint: /metrics
    health_check: /health
    log_level: INFO
```

### Monitoring and Alerting
```
Key Metrics:
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx responses)
- Database connection pool utilization
- Memory and CPU usage
- Queue depth and processing time

Alert Thresholds:
- Error rate > 1% for 5 minutes
- Response time p95 > 500ms for 10 minutes
- Database connections > 80% for 15 minutes
```

## Risk Assessment Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Database failure | Medium | High | Primary/replica setup with automated failover |
| Traffic spike | High | Medium | Auto-scaling groups with CloudWatch triggers |
| Security breach | Low | Critical | WAF, rate limiting, security scanning, audit logs |
| Third-party API failure | Medium | Medium | Circuit breakers, fallback mechanisms |

## Implementation Phases

**Phase 1** (Weeks 1-4): Core API development, basic database schema
**Phase 2** (Weeks 5-8): Authentication system, caching layer
**Phase 3** (Weeks 9-12): Performance optimization, monitoring setup
**Phase 4** (Weeks 13-16): Security hardening, load testing, deployment

Each design document should be living documentation, updated as the system evolves, and serve as the single source of truth for architectural decisions.
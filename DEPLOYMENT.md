# MOSAR GraphRAG - Deployment Guide

**Version**: 1.1.0
**Last Updated**: 2025-10-30
**Target Environments**: Development, Staging, Production

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Hardware:**
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB available space

**Software:**
- Python 3.11+ (tested on 3.11.8)
- Poetry 2.0+ for dependency management
- Neo4j Aura account (or local Neo4j 5.14+)
- OpenAI API key (GPT-4o access)

**Network:**
- Internet access for OpenAI API calls
- HTTPS access to Neo4j Aura (or local Neo4j on port 7687)

---

## Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd ReqEng
```

### 2. Install Dependencies

```bash
# Using Poetry (recommended)
poetry install

# Activate Poetry shell
poetry shell
```

### 3. Configure Environment

Create `.env` file in project root:

```bash
# Copy from example
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

**Required `.env` variables:**

```bash
# Neo4j Configuration
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

# OpenAI Configuration
OPENAI_API_KEY=sk-...your-key...

# Application Settings
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.3

# Advanced Features (Phase 5)
USE_TEXT2CYPHER=true
HITL_ENABLED=false
STREAMING_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

### 4. Load Data (First Time Only)

```bash
# Run data ingestion pipeline
poetry run python -m src.ingestion.load_all_documents

# Verify data loaded
poetry run python -m src.utils.validate_graph
```

**Expected Output:**
```
✓ Documents loaded: 4 (SRD, PDD, DDD, Demo)
✓ Nodes created: ~800
✓ Relationships created: ~1,450
✓ Vector index created: chunk_embeddings (3072 dimensions)
✓ Constraints validated: 12
```

### 5. Run Application

```bash
# Start Streamlit UI
poetry run streamlit run streamlit_app.py

# Or use shorthand
poetry run streamlit run streamlit_app.py --server.port 8501
```

Access at: http://localhost:8501

---

## Production Deployment

### Option 1: Streamlit Cloud (Recommended)

**Steps:**

1. **Prepare Repository**
   ```bash
   # Ensure requirements.txt is up to date
   poetry export -f requirements.txt --output requirements.txt --without-hashes

   # Commit changes
   git add requirements.txt
   git commit -m "Update requirements for Streamlit Cloud"
   git push
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Connect your GitHub repository
   - Select `streamlit_app.py` as main file
   - Configure secrets in Streamlit Cloud dashboard:
     ```toml
     # .streamlit/secrets.toml
     NEO4J_URI = "neo4j+s://..."
     NEO4J_USERNAME = "neo4j"
     NEO4J_PASSWORD = "..."
     NEO4J_DATABASE = "neo4j"
     OPENAI_API_KEY = "sk-..."
     ```

3. **Deploy**
   - Click "Deploy" button
   - Wait for build (~5 minutes)
   - Access your app at https://your-app.streamlit.app

**Pros:**
- ✅ Free for public repos
- ✅ Auto-deploy on git push
- ✅ Built-in HTTPS
- ✅ No server management

**Cons:**
- ⚠️ Resource limits (1GB RAM)
- ⚠️ Sleep mode after inactivity

---

### Option 2: Docker (Coming Soon)

**Note**: Docker support planned for v2.0.0

---

### Option 3: Traditional Server (Linux)

**For Ubuntu 22.04 LTS:**

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip

# 2. Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 3. Clone and setup
git clone <repo-url> /opt/mosar-graphrag
cd /opt/mosar-graphrag
poetry install --no-dev

# 4. Configure environment
cp .env.example .env
nano .env  # Add credentials

# 5. Create systemd service
sudo nano /etc/systemd/system/mosar-graphrag.service
```

**Service file:**
```ini
[Unit]
Description=MOSAR GraphRAG Streamlit Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mosar-graphrag
Environment="PATH=/opt/mosar-graphrag/.venv/bin"
ExecStart=/opt/mosar-graphrag/.venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable mosar-graphrag
sudo systemctl start mosar-graphrag

# 7. Check status
sudo systemctl status mosar-graphrag
```

**Setup Nginx reverse proxy:**

```nginx
# /etc/nginx/sites-available/mosar-graphrag
server {
    listen 80;
    server_name mosar.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/mosar-graphrag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d mosar.yourdomain.com
```

---

## Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEO4J_URI` | ✅ | - | Neo4j connection URI |
| `NEO4J_USERNAME` | ✅ | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | ✅ | - | Neo4j password |
| `NEO4J_DATABASE` | ❌ | `neo4j` | Database name |
| `OPENAI_API_KEY` | ✅ | - | OpenAI API key |
| `EMBEDDING_MODEL` | ❌ | `text-embedding-3-large` | Embedding model |
| `EMBEDDING_DIMENSIONS` | ❌ | `3072` | Vector dimensions |
| `LLM_MODEL` | ❌ | `gpt-4o` | LLM for synthesis |
| `LLM_TEMPERATURE` | ❌ | `0.3` | LLM temperature |
| `USE_TEXT2CYPHER` | ❌ | `true` | Enable Text2Cypher |
| `HITL_ENABLED` | ❌ | `false` | Enable HITL review |
| `STREAMING_ENABLED` | ❌ | `true` | Enable streaming |
| `LOG_LEVEL` | ❌ | `INFO` | Logging level |

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
```

---

## Monitoring & Maintenance

### Health Checks

**Application Health:**
```bash
# Check if Streamlit is running
curl http://localhost:8501/_stcore/health

# Expected: 200 OK
```

**Neo4j Health:**
```bash
# Using cypher-shell
poetry run python -c "from src.utils.neo4j_client import Neo4jClient; client = Neo4jClient(); print('✓ Connected' if client.verify_connection() else '✗ Failed')"
```

**OpenAI API:**
```bash
# Test API key
poetry run python -c "import openai; import os; openai.api_key = os.getenv('OPENAI_API_KEY'); print(openai.Model.list()['data'][0]['id'])"
```

### Logging

**Application Logs:**
```bash
# Streamlit logs (if running as service)
sudo journalctl -u mosar-graphrag -f

# Application logs
tail -f logs/graphrag.log
```

**Log Rotation:**
```bash
# /etc/logrotate.d/mosar-graphrag
/opt/mosar-graphrag/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### Performance Monitoring

**Key Metrics to Track:**
- Response time (target: <2s)
- OpenAI API calls per hour
- Neo4j query latency
- Memory usage
- Error rate

**Using Streamlit:**
- Query history in sidebar
- Performance tab shows processing time
- Session statistics

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'fuzzywuzzy'"

**Solution:**
```bash
poetry add fuzzywuzzy python-levenshtein
```

#### 2. Neo4j Connection Failed

**Symptoms:**
```
Neo4jError: Unable to connect to neo4j+s://...
```

**Solutions:**
- Verify URI, username, password in `.env`
- Check Neo4j Aura instance is running
- Ensure IP whitelist includes your server IP
- Test connection:
  ```bash
  poetry run python -c "from src.utils.neo4j_client import Neo4jClient; Neo4jClient().verify_connection()"
  ```

#### 3. OpenAI API Rate Limit

**Symptoms:**
```
openai.error.RateLimitError: Rate limit exceeded
```

**Solutions:**
- Reduce concurrent queries
- Upgrade OpenAI API tier
- Implement request queuing
- Enable caching for frequent queries

#### 4. Vector Search Returns Empty Results

**Check:**
```bash
# Verify vector index exists
poetry run python -c "from src.utils.neo4j_client import Neo4jClient; client = Neo4jClient(); indexes = client.execute('SHOW INDEXES'); print([i for i in indexes if 'vector' in i.get('type', '')])"
```

**Rebuild index if needed:**
```bash
poetry run python -m src.ingestion.rebuild_vector_index
```

#### 5. Streamlit "Please enter a question!" Error

**Cause**: Example question buttons may have state issue

**Workaround**: Manually type question instead of using buttons

**Fix**: Restart Streamlit app

#### 6. Slow Query Performance (>5s)

**Diagnostics:**
```bash
# Check Neo4j query performance
# In Neo4j Browser: EXPLAIN <your-query>
# Look for missing indexes or full table scans
```

**Solutions:**
- Create missing indexes
- Reduce `top_k` parameter (try k=5 instead of k=10)
- Use Entity Dictionary aggressively (avoid vector search)
- Enable query caching

---

## Security Best Practices

### API Keys
- ✅ Never commit `.env` to git
- ✅ Use environment variables or secrets management
- ✅ Rotate keys every 90 days
- ✅ Use separate keys for dev/staging/prod

### Neo4j
- ✅ Use strong passwords (16+ characters)
- ✅ Enable IP whitelist in Neo4j Aura
- ✅ Use SSL/TLS connections only
- ✅ Regular backups (Neo4j Aura auto-backup)

### Streamlit
- ✅ Enable XSRF protection
- ✅ Use HTTPS in production
- ✅ Disable usage statistics collection
- ✅ Implement authentication if public-facing

---

## Backup & Recovery

### Neo4j Backups

**Neo4j Aura:** Automatic daily backups (7-day retention)

**Self-Hosted Neo4j:**
```bash
# Create backup
neo4j-admin dump --database=neo4j --to=/backups/neo4j-$(date +%Y%m%d).dump

# Restore backup
neo4j-admin load --database=neo4j --from=/backups/neo4j-20251030.dump --force
```

### Code Backups

```bash
# Git repository (recommended)
git push origin master

# Or manual backup
tar -czf mosar-graphrag-backup-$(date +%Y%m%d).tar.gz /opt/mosar-graphrag
```

---

## Scaling

### Vertical Scaling (Single Server)

**For higher load:**
- Upgrade server RAM (16GB → 32GB)
- Increase Neo4j connection pool size
- Enable query result caching
- Optimize vector index parameters

### Horizontal Scaling (Future)

**Planned for v2.0.0:**
- Load balancer for multiple Streamlit instances
- Redis for shared session state
- Neo4j cluster (Enterprise)
- Celery for async query processing

---

## Updating

### Minor Updates (1.x.y → 1.x.z)

```bash
# Pull latest code
git pull origin master

# Update dependencies
poetry install

# Restart service
sudo systemctl restart mosar-graphrag  # or restart Streamlit manually
```

### Major Updates (1.x → 2.x)

**See CHANGELOG.md for breaking changes and migration guide**

```bash
# Backup first!
neo4j-admin dump --database=neo4j --to=/backups/pre-upgrade.dump

# Update code
git pull origin master

# Update dependencies
poetry install

# Run migrations (if any)
poetry run python -m src.migrations.run_all

# Restart
sudo systemctl restart mosar-graphrag
```

---

## Support

### Getting Help

1. **Check Documentation**:
   - [README.md](README.md) - Project overview
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
   - [CLAUDE.md](CLAUDE.md) - Development guide

2. **Review Logs**:
   - Streamlit logs: `sudo journalctl -u mosar-graphrag`
   - Application logs: `logs/graphrag.log`

3. **Known Issues**:
   - [BUGFIX_QUERY_PATH_ROUTING.md](BUGFIX_QUERY_PATH_ROUTING.md)
   - [TEST_REPORT_QUERY_PATH_FIX.md](TEST_REPORT_QUERY_PATH_FIX.md)

4. **Contact**:
   - Create GitHub issue with logs and environment details

---

## Appendix

### A. Poetry Commands Reference

```bash
# Install dependencies
poetry install

# Add new package
poetry add <package-name>

# Remove package
poetry remove <package-name>

# Update all packages
poetry update

# Export requirements
poetry export -f requirements.txt --output requirements.txt

# Run command in virtual env
poetry run <command>

# Activate shell
poetry shell
```

### B. Neo4j Cypher Queries Reference

```cypher
-- Check database stats
CALL apoc.meta.stats()

-- List all node labels
CALL db.labels()

-- List all relationship types
CALL db.relationshipTypes()

-- Show indexes
SHOW INDEXES

-- Check vector index
CALL db.index.vector.queryNodes('chunk_embeddings', 1, [0.1, 0.2, ...])

-- Count nodes by label
MATCH (n:Requirement) RETURN count(n)

-- Verify relationships
MATCH ()-[r]->() RETURN type(r), count(*) ORDER BY count(*) DESC
```

### C. Useful Debugging Scripts

**Test OpenAI Connection:**
```bash
poetry run python -c "from src.utils.embeddings import get_embedding; print(len(get_embedding('test')))"
```

**Test Neo4j Vector Search:**
```bash
poetry run python -m src.query.test_vector_search
```

**Validate Graph Integrity:**
```bash
poetry run python -m src.utils.validate_graph --full
```

---

**Document Version**: 1.0
**Last Review**: 2025-10-30
**Next Review**: 2026-01-30

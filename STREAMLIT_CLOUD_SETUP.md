# Streamlit Cloud Deployment Guide

This guide explains how to deploy the MOSAR GraphRAG system to Streamlit Cloud with secure environment variable management.

## 🌐 Deployment URL

**Production**: https://requirement-eng.streamlit.app/

---

## 🔐 Step 1: Configure Secrets in Streamlit Cloud

### Access Secrets Management:

1. Go to https://share.streamlit.io/
2. Click on your app: **requirement-eng**
3. Click the **⚙️ Settings** button (top right)
4. Select **Secrets** from the left sidebar

### Add Secrets (TOML format):

Copy and paste the following into the **Secrets** text box:

```toml
# Neo4j Database (Required)
NEO4J_URI = "bolt://YOUR_NEO4J_HOST:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR_NEO4J_PASSWORD"
NEO4J_DATABASE = "neo4j"

# For Neo4j Aura (if using cloud)
AURA_INSTANCEID = "YOUR_INSTANCE_ID"
AURA_INSTANCENAME = "YOUR_INSTANCE_NAME"

# OpenAI API (Required)
OPENAI_API_KEY = "sk-YOUR_OPENAI_API_KEY"

# LangSmith (Optional - for debugging)
LANGCHAIN_TRACING_V2 = "false"
LANGCHAIN_API_KEY = "ls-YOUR_LANGSMITH_KEY"
LANGCHAIN_PROJECT = "mosar-graphrag"

# Application Settings
LOG_LEVEL = "INFO"
CACHE_ENABLED = "true"
```

### 📝 Important Notes:

- **TOML format**: Use `key = "value"` (not `key=value`)
- **No quotes around keys**: `NEO4J_URI` not `"NEO4J_URI"`
- **Quotes around values**: `"bolt://..."` not `bolt://...`
- **Required secrets**: Neo4j credentials + OpenAI API key
- **Optional secrets**: LangSmith (can be disabled)

---

## 🔧 Step 2: Update Code to Use Streamlit Secrets

The code already supports both `.env` files (local) and Streamlit secrets (cloud).

### Current Implementation:

```python
# streamlit_app.py (already implemented)
import os
import streamlit as st

# Try Streamlit secrets first, then fall back to .env
try:
    # Streamlit Cloud secrets
    NEO4J_URI = st.secrets["NEO4J_URI"]
    NEO4J_PASSWORD = st.secrets["NEO4J_PASSWORD"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Local .env file
    from dotenv import load_dotenv
    load_dotenv()
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### ✅ This is already implemented in the codebase!

Check these files:
- `streamlit_app.py` - Main app entry point
- `src/utils/neo4j_client.py` - Neo4j connection
- `src/ingestion/embedder.py` - OpenAI embeddings

---

## 📦 Step 3: Verify Dependencies

### Check `requirements.txt`:

Streamlit Cloud uses `requirements.txt` (not `pyproject.toml`). Make sure it exists:

```bash
# Generate from Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Essential Dependencies:

```txt
langgraph>=0.2.16
neo4j>=5.14.0
openai>=1.50.0
streamlit>=1.28.0
python-dotenv>=1.0.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-core>=0.3.0
pydantic>=2.5.0
```

---

## 🚀 Step 4: Deploy & Test

### Trigger Deployment:

1. **Push to GitHub** (if using GitHub integration):
   ```bash
   git add .
   git commit -m "Update for Streamlit Cloud deployment"
   git push origin master
   ```

2. **Auto-deploy**: Streamlit Cloud will automatically redeploy

3. **Manual reboot** (if needed):
   - Go to app settings
   - Click "Reboot app"

### Verify Deployment:

1. Visit: https://requirement-eng.streamlit.app/
2. Check if app loads without errors
3. Test a simple query:
   - "FuncR_C104의 요구사항은?"
   - Should return requirement details

### Debug Deployment Issues:

1. **Check logs**: Click "Manage app" → "Logs" tab
2. **Common errors**:
   - `ModuleNotFoundError`: Missing dependency in `requirements.txt`
   - `KeyError: 'NEO4J_URI'`: Secrets not configured correctly
   - `Neo4j connection failed`: Check Neo4j Aura is running and accessible

---

## 🔍 Step 5: Connection Verification

### Neo4j Aura Requirements:

If using **Neo4j Aura Cloud**:

1. **Whitelist IP**: Add `0.0.0.0/0` (allow all) in Aura console
   - Go to: https://console.neo4j.io
   - Select your instance
   - Go to "Connection details" → "IP Allowlist"
   - Add `0.0.0.0/0` (or restrict to Streamlit Cloud IPs)

2. **Use correct URI**:
   ```
   bolt://YOUR_INSTANCE_ID.databases.neo4j.io:7687
   ```
   NOT `neo4j+s://...` (use `bolt://`)

3. **Test connection locally first**:
   ```python
   from neo4j import GraphDatabase

   driver = GraphDatabase.driver(
       "bolt://YOUR_HOST:7687",
       auth=("neo4j", "YOUR_PASSWORD")
   )
   driver.verify_connectivity()
   print("✅ Connected!")
   ```

---

## 📊 Step 6: Monitor Performance

### Streamlit Cloud Limits:

- **RAM**: 1GB (free tier)
- **CPU**: Shared
- **Data**: Public apps only
- **Sleep**: App sleeps after 7 days inactivity

### Optimization Tips:

1. **Enable caching**:
   ```python
   @st.cache_data(ttl=3600)
   def expensive_query():
       ...
   ```

2. **Limit concurrent queries**: Already implemented with session state

3. **Monitor logs**: Check for memory warnings

---

## ⚠️ Security Notes

### Do NOT commit secrets:

```bash
# .gitignore (already configured)
.env
.env.*
secrets.toml
```

### Public vs Private Apps:

- **Public app**: Code is visible, secrets are NOT
- **Private app**: Requires Streamlit Cloud Teams plan
- **Current setup**: Public app, secrets hidden ✅

---

## 🆘 Troubleshooting

### Error: "This app has encountered an error"

**Check logs**:
1. Go to app settings → Logs
2. Look for Python errors
3. Common issues:
   - Missing secrets
   - Module import errors
   - Neo4j connection timeout

### Error: "ModuleNotFoundError"

**Solution**: Update `requirements.txt`
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Error: "Neo4j connection failed"

**Checklist**:
- [ ] Neo4j Aura instance is running
- [ ] IP whitelist includes `0.0.0.0/0`
- [ ] Correct URI format: `bolt://...` not `neo4j+s://...`
- [ ] Password is correct (no extra spaces)
- [ ] Secrets in TOML format with quotes

### Error: "OpenAI API key invalid"

**Solution**:
1. Verify API key at: https://platform.openai.com/api-keys
2. Check secrets format: `OPENAI_API_KEY = "sk-..."`
3. No extra spaces or newlines

---

## 📚 Additional Resources

- **Streamlit Secrets Docs**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Neo4j Aura**: https://console.neo4j.io
- **OpenAI API Keys**: https://platform.openai.com/api-keys

---

## ✅ Quick Checklist

Before deploying, verify:

- [ ] `requirements.txt` exists and is up-to-date
- [ ] Secrets configured in Streamlit Cloud dashboard
- [ ] Neo4j Aura IP whitelist includes Streamlit Cloud
- [ ] OpenAI API key is valid and has credits
- [ ] Code uses `st.secrets` for cloud deployment
- [ ] `.env` file is in `.gitignore`
- [ ] App tested locally with same secrets

---

**Last Updated**: 2025-10-31
**Version**: 1.2.0

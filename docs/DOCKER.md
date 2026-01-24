# Web API Reference & Operations

Advanced Docker operations, production deployment, and API details for AlongGPX.

**Getting started?** See [quickstart-docker.md](quickstart-docker.md) for setup and configuration.

---

## API Reference

### Health Check
```bash
GET /health
```
Simple status endpoint for monitoring. Returns 200 if container is healthy.

### Process GPX File
```bash
POST /api/process
Content-Type: multipart/form-data
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | GPX file (*.gpx) |
| `project_name` | String | No | Output filename prefix (default: from config) |
| `radius_km` | Float | No | Search radius in km (default: 5) |
| `step_km` | Float | No | Distance between query points (default: 60% of radius) |
| `include` | String | No | Include filter, e.g., `tourism=camp_site` (repeatable) |
| `exclude` | String | No | Exclude filter, e.g., `tents=no` (repeatable) |

**Example:**
```bash
curl -F "file=@track.gpx" \
     -F "project_name=MyTrip" \
     -F "radius_km=5" \
     -F "include=tourism=camp_site" \
     -F "exclude=tents=no" \
     http://localhost:5000/api/process
```

**Response:**
```json
{
  "success": true,
  "excel_file": "MyTrip_20260124_120000.xlsx",
  "html_file": "MyTrip_20260124_120000.html",
  "excel_path": "/app/data/output/MyTrip_20260124_120000.xlsx",
  "html_path": "/app/data/output/MyTrip_20260124_120000.html",
  "rows_count": 42,
  "track_length_km": 125.5
}
```

---

## Operations & Debugging

### Test Locally (No Docker)
```bash
# CLI mode
python3 cli/main.py --gpx-file ./data/input/track.gpx --radius-km 5

# Web API in development mode
export FLASK_ENV=development
python -m flask --app docker.app run --port 5000
```

### Debugging
Enable debug mode in docker-compose.yml:
```yaml
environment:
  - FLASK_ENV=development
```

Then restart: `docker-compose up -d --build`

---

## Production Deployment

### Use Gunicorn (Production Web Server)
Replace Flask's dev server with Gunicorn for concurrent request handling:

Edit `docker/Dockerfile`:
```dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "docker.app:app"]
```

Rebuild: `docker-compose up -d --build`

### Reverse Proxy (Nginx)
For SSL/TLS and multiple replicas:

```nginx
upstream alonggpx {
    server localhost:5000;
}

server {
    listen 443 ssl;
    server_name gpx.example.com;
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://alonggpx;
        proxy_set_header Host $host;
        client_max_body_size 50M;
    }
}
```

---

## Architecture & Design

**Multi-stage Docker build:**
- Base stage: Installs dependencies, builds wheels
- Production stage: Copies only runtime (smaller image ~300MB)

**Security:**
- Runs as non-root user (`alonggpx`, UID 1000)
- Input directory is read-only
- No hardcoded credentials

**Health checks:**
- Polls `/health` endpoint every 30s
- Fails fast if container becomes unhealthy

**Volume mounts:**
- `../data/input:ro` (read-only): Protects source GPX files
- `../data/output:rw` (read-write): Container writes results to host

---

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `Flask 3.0.0` | REST API framework |
| `gpxpy` | GPX parsing |
| `shapely` | Geometric operations |
| `pyproj` | Geodetic distance (WGS84 ellipsoid) |
| `requests` | HTTP to Overpass API |
| `folium` | Interactive map generation |
| `pandas` | DataFrame & Excel export |
| `python-dotenv` | Environment variable loading |

### Viewing Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50

# With timestamps
docker-compose logs --timestamps
```

### Manual Build
If not using `docker-compose`, build and run manually:

```bash
cd docker
docker build -t alonggpx:latest ..

docker run -p 5000:5000 \
  -v "$(pwd)/../data/input:/app/data/input:ro" \
  -v "$(pwd)/../data/output:/app/data/output:rw" \
  -e ALONGGPX_RADIUS_KM=5 \
  alonggpx:latest
```


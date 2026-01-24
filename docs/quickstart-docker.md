# Quickstart (Docker)

Run AlongGPX as a web API with Docker and Docker Compose in ~2 minutes.

## Prerequisites
- Docker ≥ 20.10
- Docker Compose ≥ 1.29

## 1) Start the Container
```bash
cd docker
docker-compose up -d
```

## 2) Verify Health
```bash
curl http://localhost:5000/health
# {"status": "healthy", "service": "AlongGPX"}
```

## 3) Process a GPX File
```bash
curl -F "file=@../data/input/track.gpx" \
     -F "project_name=MyTrip" \
     -F "radius_km=5" \
     http://localhost:5000/api/process
```

Results are saved to `../data/output/`.

## Configuration

By default, the container uses `../config.yaml` (auto-mounted from repo root). For most setups, no extra configuration is required.

- Precedence: environment variables (optional overrides) > `config.yaml` defaults
- Volume mounts: `../data/input` (read-only), `../data/output` (read-write)

Optional environment overrides:

Method A: `.env` file
```bash
# docker/.env
ALONGGPX_RADIUS_KM=8
ALONGGPX_BATCH_KM=60
ALONGGPX_TIMEZONE=Europe/Berlin
```

Method B: `docker-compose.yml`
```yaml
services:
  alonggpx:
    environment:
      - ALONGGPX_RADIUS_KM=8
      - ALONGGPX_BATCH_KM=60
```

## Troubleshooting
- Wait 10s after `up -d` (health checks)
- Check container logs: `docker-compose logs -f`
- Ensure GPX exists in `../data/input/`
- If port 5000 is used: change to `ports: ["5001:5000"]`

## Next Steps
- See full API details in `docs/DOCKER.md`
- Adjust defaults in `config.yaml`
- Explore or add presets in `presets.yaml`

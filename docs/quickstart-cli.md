# Quickstart (CLI)

Run AlongGPX locally via the command line in about 5 minutes.

## Prerequisites
- Python 3.8+ (`python3 --version`)
- pip (`python3 -m pip --version`)

## 1) Create a Virtual Environment (Recommended)

Using a venv keeps your system Python clean.

Linux/macOS:
```bash
cd AlongGPX
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):
```powershell
cd AlongGPX
python -m venv venv
venv\Scripts\Activate.ps1
```

Your prompt should show `(venv)`.

## 2) Install Dependencies
```bash
pip install -r requirements-base.txt
```

## 3) First Run
```bash
python3 cli/main.py --preset camp_basic
```
Results are saved to `data/output/`.

## 4) Customize
```bash
# Change search radius
python3 cli/main.py --radius-km 10 --preset camp_basic

# Multiple includes
python3 cli/main.py \
  --preset camp_basic \
  --include amenity=drinking_water \
  --include amenity=shelter \
  --project-name MyTrip

# Use a specific GPX file
python3 cli/main.py --gpx-file ./data/input/track.gpx --preset drinking_water
```

## Configuration & Presets
- Defaults: `config.yaml`
- Presets: `presets.yaml`
- Precedence: CLI args > environment variables > config.yaml

Optional environment overrides:
```bash
export ALONGGPX_RADIUS_KM=8
export ALONGGPX_BATCH_KM=50
python3 cli/main.py --preset camp_basic
```

## Common Presets
```bash
--preset camp_basic        # Campsites (tents allowed)
--preset accommodation     # Hotels, B&Bs, guest houses
--preset drinking_water    # Water sources
--preset shelters          # Emergency shelters
```

## Troubleshooting
- Run from repo root (`cd AlongGPX`)
- Check filter syntax: `key=value`
- If Overpass times out, reduce query complexity or adjust `batch_km` in `config.yaml`

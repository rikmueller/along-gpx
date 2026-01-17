import gpxpy
from pyproj import Geod


def load_gpx_track(gpx_file: str):
    """
    Lädt eine GPX-Datei und gibt eine Liste von (lon, lat)-Punkten zurück.
    """
    with open(gpx_file, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    track_points = [
        (p.longitude, p.latitude)
        for t in gpx.tracks
        for s in t.segments
        for p in s.points
    ]

    if not track_points:
        raise ValueError(f"Keine Trackpunkte in {gpx_file} gefunden.")

    return track_points


def compute_track_metrics(track_points):
    """
    Berechnet geodätische Streckenlänge und kumulative Distanzen.
    """
    geod = Geod(ellps="WGS84")

    distances_km = [0.0]
    total_m = 0.0

    for i in range(1, len(track_points)):
        lon1, lat1 = track_points[i - 1]
        lon2, lat2 = track_points[i]
        _, _, d = geod.inv(lon1, lat1, lon2, lat2)
        total_m += d
        distances_km.append(total_m / 1000)

    total_track_length_km = distances_km[-1]

    return {
        "distances_km": distances_km,
        "total_length_km": total_track_length_km,
    }

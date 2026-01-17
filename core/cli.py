import argparse


def parse_cli_args():
    """
    CLI-Argumente definieren und einlesen.
    YAML-Config kann überschrieben/ergänzt werden.
    """
    parser = argparse.ArgumentParser(
        description="Finde OSM-Objekte entlang eines GPX-Tracks (Overpass, Excel, Folium)."
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Pfad zur YAML-Konfigurationsdatei (Default: config.yaml)",
    )

    parser.add_argument(
        "--project-name",
        type=str,
        help="Projektname, überschreibt project.name aus config.yaml",
    )

    parser.add_argument(
        "--output-path",
        type=str,
        help="Output-Pfad, überschreibt project.output_path aus config.yaml",
    )

    parser.add_argument(
        "--gpx-file",
        type=str,
        help="GPX-Datei, überschreibt input.gpx_file aus config.yaml",
    )

    parser.add_argument(
        "--radius-km",
        type=float,
        help="Suchradius in km, überschreibt search.radius_km",
    )

    parser.add_argument(
        "--step-km",
        type=float,
        help="Abstand der Overpass-Abfragen in km, überschreibt search.step_km",
    )

    parser.add_argument(
        "--include",
        action="append",
        default=None,
        help="Zusätzlicher Include-Filter (key=value). Mehrfach nutzbar.",
    )

    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        help="Zusätzlicher Exclude-Filter (key=value). Mehrfach nutzbar.",
    )

    parser.add_argument(
        "--preset",
        dest="presets",
        action="append",
        default=None,
        help="Name eines Presets aus presets.yaml. Mehrfach nutzbar.",
    )

    return parser.parse_args()

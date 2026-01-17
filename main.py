#!/usr/bin/env python3
import sys
from core.cli import parse_cli_args
from core.config import load_and_merge_config
from core.presets import load_presets, apply_presets_to_filters
from core.gpx_processing import load_gpx_track, compute_track_metrics
from core.overpass import query_overpass_segmented
from core.filtering import filter_elements_and_build_rows
from core.export import export_to_excel
from core.folium_map import build_folium_map


def main():
    # CLI-Argumente einlesen
    args = parse_cli_args()

    # Konfiguration aus YAML + CLI mergen
    config = load_and_merge_config(args.config, args)

    # Presets laden
    presets = load_presets(config.get("presets_file", "presets.yaml"))

    # Presets auf include/exclude anwenden
    include_filters, exclude_filters = apply_presets_to_filters(
        presets,
        config["search"]["include"],
        config["search"]["exclude"],
        args.presets,
        args.include,
        args.exclude,
    )

    # GPX laden und Track vorbereiten
    track_points = load_gpx_track(config["input"]["gpx_file"])
    track_info = compute_track_metrics(track_points)

    # Overpass-Abfragen entlang des Tracks
    elements = query_overpass_segmented(
        track_points=track_points,
        track_info=track_info,
        radius_km=config["search"]["radius_km"],
        step_km=config["search"]["step_km"],
        overpass_cfg=config["overpass"],
        include_filters=include_filters,
    )

    # Elemente filtern und tabellarische Daten erzeugen
    rows, df = filter_elements_and_build_rows(
        elements=elements,
        track_points=track_points,
        track_info=track_info,
        radius_km=config["search"]["radius_km"],
        exclude_filters=exclude_filters,
    )

    # Excel exportieren
    excel_path = export_to_excel(
        df=df,
        output_path=config["project"]["output_path"],
        project_name=config["project"]["name"],
    )

    # Folium-Karte erzeugen
    html_path = build_folium_map(
        df=df,
        track_points=track_points,
        output_path=config["project"]["output_path"],
        project_name=config["project"]["name"],
        map_cfg=config["map"],
    )

    print(f"✅ Fertig! {len(df)} Objekte gefunden.")
    print(f"📄 Excel: {excel_path}")
    print(f"🗺️ Karte: {html_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Abgebrochen durch Benutzer.")
        sys.exit(1)

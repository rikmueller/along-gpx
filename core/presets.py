import yaml


def load_presets(path: str) -> dict:
    """
    Lädt presets.yaml und gibt ein Dict zurück.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("presets", {})


def validate_filter_syntax(filter_str: str):
    """
    Validiert, dass ein Filter die Form key=value hat.
    """
    if "=" not in filter_str:
        raise ValueError(f"Ungültiger Filter (erwartet key=value): {filter_str}")
    key, value = filter_str.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key or not value:
        raise ValueError(f"Ungültiger Filter (leerer key oder value): {filter_str}")
    return key, value


def apply_presets_to_filters(
    presets: dict,
    base_include: list,
    base_exclude: list,
    preset_names: list | None,
    cli_include: list | None,
    cli_exclude: list | None,
):
    """
    Kombiniert:
    - Basis-Filter aus config.yaml
    - Presets aus presets.yaml
    - zusätzliche CLI-Filter
    und validiert die Syntax.
    """
    include = list(base_include or [])
    exclude = list(base_exclude or [])

    # Presets anwenden
    if preset_names:
        for name in preset_names:
            if name not in presets:
                raise ValueError(f"Preset '{name}' nicht in presets.yaml gefunden.")
            p = presets[name]
            include.extend(p.get("include", []))
            exclude.extend(p.get("exclude", []))

    # CLI-Filter hinzufügen
    if cli_include:
        include.extend(cli_include)
    if cli_exclude:
        exclude.extend(cli_exclude)

    # Duplikate entfernen
    include = list(dict.fromkeys(include))
    exclude = list(dict.fromkeys(exclude))

    # Validierung
    for f in include + exclude:
        validate_filter_syntax(f)

    return include, exclude

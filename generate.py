import json
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)


def write_page(env, template_name, output_path, context):
    template = env.get_template(template_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.render(**context), encoding="utf-8")


def main():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    city_data = load_yaml(CONTENT_DIR / "city.yaml")["city"]
    map_settings = load_yaml(CONTENT_DIR / "city.yaml")["map"]
    places = load_yaml(CONTENT_DIR / "places.yaml")["places"]
    parks = load_yaml(CONTENT_DIR / "parks.yaml")["parks"]
    bars = load_yaml(CONTENT_DIR / "bars.yaml")["bars"]
    clubs = load_yaml(CONTENT_DIR / "clubs.yaml")["clubs"]
    restaurants = load_yaml(CONTENT_DIR / "restaurants.yaml")["restaurants"]
    cafes = load_yaml(CONTENT_DIR / "cafes.yaml")["cafes"]
    museums = load_yaml(CONTENT_DIR / "museums.yaml")["museums"]
    typical_food = load_yaml(CONTENT_DIR / "food_typical.yaml")["typical_food"]
    phrases = load_yaml(CONTENT_DIR / "phrases.yaml")["phrases"]
    history_page = load_yaml(CONTENT_DIR / "history.yaml")["history"]
    agenda = load_yaml(CONTENT_DIR / "agenda.yaml")["agenda"]
    schedule = load_yaml(CONTENT_DIR / "schedule.yaml")["schedule"]

    ensure_dir(DIST_DIR)

    # Copy static assets
    if (DIST_DIR / "static").exists():
        shutil.rmtree(DIST_DIR / "static")
    shutil.copytree(STATIC_DIR, DIST_DIR / "static")

    base_context = {
        "city": city_data,
        "places": places,
        "parks": parks,
        "bars": bars,
        "clubs": clubs,
        "restaurants": restaurants,
        "cafes": cafes,
        "museums": museums,
        "typical_food": typical_food,
        "phrases": phrases,
        "history": history_page,
        "agenda": agenda,
    }

    # Home page
    write_page(
        env,
        "index.html",
        DIST_DIR / "index.html",
        {
            **base_context,
            "page_title": "Home",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    # Schedule page
    write_page(
        env,
        "schedule.html",
        DIST_DIR / "schedule.html",
        {
            **base_context,
            "schedule": schedule,
            "page_title": "Schedule",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    # Map page
    map_points = []
    for item in places:
        map_points.append(
            {
                "type": "places",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"places/{item['id']}.html",
            }
        )
    for item in parks:
        map_points.append(
            {
                "type": "parks",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"parks/{item['id']}.html",
            }
        )
    for item in museums:
        map_points.append(
            {
                "type": "museums",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"museums/{item['id']}.html",
            }
        )
    for item in restaurants:
        map_points.append(
            {
                "type": "restaurants",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"restaurants/{item['id']}.html",
            }
        )
    for item in cafes:
        map_points.append(
            {
                "type": "cafes",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"cafes/{item['id']}.html",
            }
        )
    for item in bars:
        map_points.append(
            {
                "type": "bars",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"bars/{item['id']}.html",
            }
        )
    for item in clubs:
        map_points.append(
            {
                "type": "clubs",
                "name": item["name"],
                "category": item["category"],
                "coordinates": item["coordinates"],
                "url": f"clubs/{item['id']}.html",
            }
        )

    map_data = json.dumps(
        {
            "center": map_settings["center"],
            "zoom": map_settings["zoom"],
            "points": map_points,
        }
    )

    write_page(
        env,
        "map.html",
        DIST_DIR / "map.html",
        {
            **base_context,
            "page_title": "Map",
            "base_prefix": "",
            "static_prefix": "static/",
            "map_data": map_data,
        },
    )

    # Extra pages
    write_page(
        env,
        "food_typical.html",
        DIST_DIR / "food-typical.html",
        {
            **base_context,
            "page_title": "Menjar típic",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    write_page(
        env,
        "phrases.html",
        DIST_DIR / "phrases.html",
        {
            **base_context,
            "page_title": "Paraules en eslovac",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    write_page(
        env,
        "history.html",
        DIST_DIR / "history.html",
        {
            **base_context,
            "page_title": "Història",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    write_page(
        env,
        "agenda.html",
        DIST_DIR / "agenda.html",
        {
            **base_context,
            "page_title": "Agenda cultural",
            "base_prefix": "",
            "static_prefix": "static/",
        },
    )

    # List pages
    list_pages = [
        ("places", places, "Llocs d'interès", "Estàtues, ponts, edificis i carrers destacats."),
        ("parks", parks, "Parcs", "Zones verdes i espais per passejar."),
        ("museums", museums, "Museus i galeries", "Cultura, art i història local."),
        ("restaurants", restaurants, "Restaurants", "Menjar local i opcions per dinar o sopar."),
        ("cafes", cafes, "Fleques i cafès", "Cafè, te i berenars tranquils."),
        ("bars", bars, "Bars i cerveseries", "Cerveses artesanes, pubs i còctels."),
        ("clubs", clubs, "Discoteques", "Música i ambient nocturn."),
    ]

    for section, items, title, intro in list_pages:
        section_dir = DIST_DIR / section
        for item in items:
            item["url"] = f"{item['id']}.html"

        write_page(
            env,
            "list.html",
            section_dir / "index.html",
            {
                **base_context,
                "items": items,
                "section_title": title,
                "section_intro": intro,
                "page_title": title,
                "base_prefix": "../",
                "static_prefix": "../static/",
            },
        )

        for item in items:
            write_page(
                env,
                "detail.html",
                section_dir / f"{item['id']}.html",
                {
                    **base_context,
                    "item": item,
                    "page_title": item["name"],
                    "back_link": "index.html",
                    "back_label": title,
                    "base_prefix": "../",
                    "static_prefix": "../static/",
                },
            )


if __name__ == "__main__":
    main()

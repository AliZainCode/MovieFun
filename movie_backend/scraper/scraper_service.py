import requests
import time
import random

from requests.exceptions import ReadTimeout, RequestException
from .models import TVSeries


FILTER_URL = "https://h5-api.aoneroom.com/wefeed-h5api-bff/subject/filter"
DETAIL_URL = "https://h5-api.aoneroom.com/wefeed-h5api-bff/detail"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://moviebox.ph",
    "referer": "https://moviebox.ph/",
    "user-agent": "Mozilla/5.0",
    "authorization": "Bearer YOUR_TOKEN_HERE"
}

BASE_PLAY_URL = "https://123movienow.cc/spa/videoPlayPage/movies/"

session = requests.Session()
session.headers.update(HEADERS)


def fetch_series_page(page=1, per_page=28, retries=3):

    for attempt in range(retries):
        try:
            response = session.post(
                FILTER_URL,
                json={"page": page, "perPage": per_page, "channelId": 2},
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"[PAGE FAILED] attempt {attempt+1}: {e}")
            time.sleep(2)

    return None


def fetch_series_detail(detail_path, retries=3):

    for attempt in range(retries):
        try:
            response = session.get(
                DETAIL_URL,
                params={"detailPath": detail_path},
                timeout=40
            )
            response.raise_for_status()
            return response.json()

        except ReadTimeout:
            print("[DETAIL TIMEOUT]")
            time.sleep(3)

        except RequestException as e:
            print(f"[REQUEST FAILED] {e}")
            break

    return None


def parse_series(item, detail):

    data = detail.get("data", {})
    subject = data.get("subject") or {}
    resource = data.get("resource") or {}
    stars = data.get("stars") or []

    genre = item.get("genre", "") or ""

    if "song" in genre.lower():
        return None

    seasons_data = resource.get("seasons", []) or []

    season_details = []
    total_episodes = 0

    for index, season in enumerate(seasons_data, start=1):
        max_ep = int(season.get("maxEp", 0))
        total_episodes += max_ep

        season_details.append({
            "season_number": index,
            "total_episodes": max_ep
        })

    if total_episodes == 0:
        return None

    cast_details = [
        {
            "name": s.get("name", ""),
            "character": s.get("character", ""),
            "avatarUrl": s.get("avatarUrl", ""),
            "detailPath": s.get("detailPath", "")
        }
        for s in stars
    ]

    trailer_url = ""

    if subject.get("trailer"):
        trailer_url = subject["trailer"].get("videoAddress", {}).get("url", "")

    subject_id = subject.get("subjectId", "")

    play_url = f"{BASE_PLAY_URL}{item.get('detailPath')}?id={subject_id}&type=/movie/detail&lang=en" if subject_id else ""

    return {
        "title": item.get("title", ""),
        "genre": genre,
        "release_date": item.get("releaseDate", ""),
        "country": item.get("countryName", ""),
        "imdb_rating": float(item.get("imdbRatingValue") or 0) or None,
        "imdb_votes": int(item.get("imdbRatingCount") or 0) or None,
        "description": subject.get("description", ""),
        "total_seasons": len(seasons_data),
        "total_episodes": total_episodes,
        "season_details": season_details,
        "cast_details": cast_details,
        "trailer_url": trailer_url,
        "cover_image": item.get("cover", {}).get("url", ""),
        "detail_path": item.get("detailPath", ""),
        "subject_id": subject_id,
        "play_url": play_url
    }


def save_to_database(data):

    obj, created = TVSeries.objects.update_or_create(
        subject_id=data["subject_id"],
        defaults=data
    )

    if created:
        print(f"[NEW] {data['title']}")
    else:
        print(f"[UPDATED] {data['title']}")


def scrape_all_series(per_page=28):

    page = 1

    while True:

        print(f"Fetching page {page}")

        response = fetch_series_page(page, per_page)

        if not response:
            break

        items = response.get("data", {}).get("items", [])

        if not items:
            print("No more series found")
            break

        for item in items:

            detail = fetch_series_detail(item.get("detailPath"))

            if not detail:
                print(f"[FAILED] {item.get('title')}")
                continue

            parsed = parse_series(item, detail)

            if parsed:
                save_to_database(parsed)
            else:
                print(f"[FAILED] {item.get('title')}")

            time.sleep(random.uniform(0.3, 0.8))

        page += 1

    print("Scraping completed successfully!")

import requests
import time
from requests.exceptions import ReadTimeout, RequestException
from .models import Movie 

FILTER_URL = "https://h5-api.aoneroom.com/wefeed-h5api-bff/subject/filter"
DETAIL_URL = "https://h5-api.aoneroom.com/wefeed-h5api-bff/detail"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://moviebox.ph",
    "referer": "https://moviebox.ph/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "authorization": "Bearer YOUR_TOKEN_HERE"
}

BASE_PLAY_URL = "https://123movienow.cc/spa/videoPlayPage/movies/"


def fetch_movie_page(page=1, per_page=28):
    response = requests.post(
        FILTER_URL,
        json={"page": page, "perPage": per_page, "channelId": 1}, 
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def fetch_movie_detail(detail_path, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                DETAIL_URL,
                params={"detailPath": detail_path},
                headers=HEADERS,
                timeout=40
            )
            response.raise_for_status()
            return response.json()

        except ReadTimeout:
            print(f"Timeout attempt {attempt}")
            time.sleep(3)

        except RequestException as e:
            print(f"Request failed: {e}")
            break

    return None


def parse_movie(item, detail):
    data = detail.get("data", {})
    subject = data.get("subject") or {}
    resource = data.get("resource") or {}
    stars = data.get("stars") or []

    genre = item.get("genre", "") or ""

    if "song" in genre.lower():
        return None

    seasons_data = resource.get("seasons", []) or []
    total_episodes = sum(int(season.get("maxEp", 0)) for season in seasons_data)


    if total_episodes > 1:
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
    play_url = (
        f"{BASE_PLAY_URL}{item.get('detailPath')}?id={subject_id}&type=/movie/detail&lang=en"
        if subject_id else ""
    )

    return {
        "title": item.get("title", ""),
        "genre": genre,
        "release_date": item.get("releaseDate", ""),
        "country": item.get("countryName", ""),
        "imdb_rating": float(item.get("imdbRatingValue") or 0) or None,
        "imdb_votes": int(item.get("imdbRatingCount") or 0) or None,
        "description": subject.get("description", ""),
        "cast_details": cast_details,
        "trailer_url": trailer_url,
        "cover_image": item.get("cover", {}).get("url", ""),
        "detail_path": item.get("detailPath", ""),
        "subject_id": subject_id,
        "play_url": play_url
    }


def save_movie(data):
    obj, created = Movie.objects.update_or_create(
        subject_id=data["subject_id"],
        defaults=data
    )

    if created:
        print(f"Saved (New): {data['title']}")
    else:
        print(f"Updated (Existing): {data['title']}")


def scrape_all_movies(per_page=28):
    page = 1

    while True:
        print(f"Fetching movie page {page}...")

        try:
            response = fetch_movie_page(page, per_page)
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            break

        items = response.get("data", {}).get("items", [])

        if not items:
            print("No more movies found.")
            break

        for item in items:
            detail = fetch_movie_detail(item.get("detailPath"))

            if not detail or not detail.get("data", {}).get("resource"):
                print(f"Skipped (no resource): {item.get('title', '')}")
                continue

            parsed = parse_movie(item, detail)

            if parsed:
                save_movie(parsed)
            else:
                print(f"Skipped (invalid movie): {item.get('title', '')}")

            time.sleep(1)

        page += 1

    print("Movie scraping completed successfully!")

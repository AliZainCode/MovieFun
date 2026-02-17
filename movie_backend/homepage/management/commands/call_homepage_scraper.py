import requests
import time
from django.core.management.base import BaseCommand
from homepage.models import homepagemodel

BASE_API = "https://h5-api.aoneroom.com/wefeed-h5api-bff"
TOKEN = "YOUR_BEARER_TOKEN_HERE"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
    "Origin": "https://moviebox.ph",
    "Referer": "https://moviebox.ph/",
}

def safe_json(r):
    try:
        return r.json()
    except:
        return None

def get_all_home_subjects():
    url = f"{BASE_API}/home?host=moviebox.ph"
    r = requests.get(url, headers=HEADERS)
    data = safe_json(r)
    if not data or data.get("code") != 0:
        return []

    subjects = {}

    for section in data.get("data", {}).get("operatingList", []):
        t = section.get("type")

        if t == "BANNER" and section.get("banner"):
            for item in section["banner"].get("items", []):
                s = item.get("subject", {})
                if s.get("subjectId"):
                    subjects[s["subjectId"]] = s

        elif t == "SUBJECTS_MOVIE":
            for s in section.get("subjects", []):
                if s.get("subjectId"):
                    subjects[s["subjectId"]] = s

    return list(subjects.values())

def get_detail(detail_path):
    url = f"{BASE_API}/detail?detailPath={detail_path}"
    r = requests.get(url, headers=HEADERS)
    data = safe_json(r)
    if not data or data.get("code") != 0:
        return None
    return data.get("data", {})

class Command(BaseCommand):

    help = "Sync homepage items"

    def handle(self, *args, **kwargs):

        print("Starting homepage sync...")

        home_subjects = get_all_home_subjects()

        new_ids = set()

        position = 1

        for subject_item in home_subjects:

            detail_path = subject_item.get("detailPath")
            if not detail_path:
                continue

            detail_data = get_detail(detail_path)
            if not detail_data:
                continue

            subject = detail_data.get("subject", {})

            subject_id = subject.get("subjectId")

            if not subject_id:
                continue

            new_ids.add(subject_id)

            stars = (
                detail_data.get("stars")
                or subject.get("stars")
                or subject.get("staffList")
                or []
            )

            clean_cast = [
                {
                    "staffId": s.get("staffId"),
                    "staffType": s.get("staffType"),
                    "name": s.get("name"),
                    "character": s.get("character"),
                    "avatarUrl": s.get("avatarUrl"),
                    "detailPath": s.get("detailPath"),
                }
                for s in stars
            ]

            play_url = f"https://123movienow.cc/spa/videoPlayPage/movies/{subject.get('detailPath')}?id={subject_id}&type=/movie/detail"

            obj, created = homepagemodel.objects.update_or_create(
                subject_id=subject_id,
                defaults={
                    "title": subject.get("title", ""),
                    "type": "Movie" if subject.get("subjectType") == 1 else "TV Series",
                    "genre": subject.get("genre", ""),
                    "release_date": subject.get("releaseDate", ""),
                    "country": subject.get("countryName", ""),
                    "description": subject.get("description", ""),
                    "imdb": subject.get("imdbRatingValue", ""),
                    "imdb_votes": subject.get("imdbRatingCount", ""),
                    "duration": subject.get("duration", ""),
                    "cast": clean_cast,
                    "trailer_url": subject.get("trailer", {}).get("videoAddress", {}).get("url", "") if subject.get("trailer") else "",
                    "cover_image": subject.get("cover", {}).get("url", ""),
                    "play_url": play_url,
                    "detail_path": subject.get("detailPath", ""),
                    "position": position,
                }
            )

            if created:
                print(f"[NEW] {subject.get('title')}")
            else:
                print(f"[UPDATED] {subject.get('title')}")

            position += 1

            time.sleep(0.5)

        deleted = homepagemodel.objects.exclude(subject_id__in=new_ids)
        deleted_count = deleted.count()
        deleted.delete()

        print(f"Removed old items: {deleted_count}")
        print("Homepage sync completed!")

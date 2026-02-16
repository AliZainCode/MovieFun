from django.core.management.base import BaseCommand
from moviescraper.movie_scraper import scrape_all_movies

class Command(BaseCommand):
    help = "Run Movie scraper and save data to database (scraper_movie)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting scraper_movie..."))
        scrape_all_movies(per_page=28)
        self.stdout.write(self.style.SUCCESS("scraper_movie completed successfully!"))

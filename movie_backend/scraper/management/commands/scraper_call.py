from django.core.management.base import BaseCommand
from scraper.scraper_service import scrape_all_series

class Command(BaseCommand):
    help = "Run TV Series scraper and save data to database (scraper_series)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting scraper_series..."))
        scrape_all_series(per_page=28)  
        self.stdout.write(self.style.SUCCESS("scraper_series completed successfully!"))

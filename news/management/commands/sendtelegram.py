from django.core.management.base import BaseCommand
from news.views import send_telegram_news

class Command(BaseCommand):
    help = 'Sends daily news to Telegram subscribers'

    def handle(self, *args, **kwargs):
        send_telegram_news()
        self.stdout.write(self.style.SUCCESS('✅ Telegram news sent.'))

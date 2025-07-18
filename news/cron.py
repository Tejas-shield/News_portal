from django_cron import CronJobBase, Schedule
from .views import send_telegram_news

class DailyNewsCron(CronJobBase):
    RUN_AT_TIMES = ['08:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'news.daily_news_cron'

    def do(self):
        send_telegram_news()

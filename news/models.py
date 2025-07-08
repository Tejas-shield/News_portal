from django.db import models

class Comment(models.Model):
    article_url = models.URLField()
    name = models.CharField(max_length=100)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.article_url[:30]}..."


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100, blank=True, null=True)  # Telegram chat ID

    def __str__(self):
        return f"{self.name} - {self.chat_id}"

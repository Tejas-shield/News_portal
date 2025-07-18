import os, requests
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import Comment, Subscription
from .forms import CommentForm, SubscriptionForm
from newspaper import Article
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

load_dotenv()

# Hugging Face Summarizer
def summarize_with_huggingface(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"
    }
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return f"Hugging Face summary error: {response.status_code} - {response.text}"

# Article content extraction
def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# Home view
def home(request):
    category = request.GET.get('category', 'general')
    query = request.GET.get('q')
    api_key = os.getenv("NEWS_API_KEY")

    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"

    news = requests.get(url).json().get("articles", [])
    return render(request, "news/home.html", {"news": news})

# Article detail + comments + summary
def article_detail(request):
    url = request.GET.get('url')
    if not url or url == "None":
        return render(request, "news/error.html", {"error": "Invalid article URL"})

    comments = Comment.objects.filter(article_url=url)
    form = CommentForm(request.POST or None)
    summary = ''

    if form.is_valid():
        obj = form.save(commit=False)
        obj.article_url = url
        obj.save()
        return redirect(request.path + f'?url={url}')

    if request.GET.get('summarize'):
        try:
            article_text = extract_article_text(url)
            summary = summarize_with_huggingface(article_text)
        except Exception as e:
            summary = f"Summarization error: {str(e)}"

    return render(request, "news/detail.html", {
        "url": url,
        "comments": comments,
        "form": form,
        "summary": summary
    })

# Subscription view
def subscribe(request):
    form = SubscriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, "news/subscribe.html", {"form": form})


def trigger_telegram_news(request):
    from .views import send_telegram_news
    send_telegram_news()
    return HttpResponse("✅ News sent to Telegram successfully!")

# ✅ TELEGRAM NEWS FUNCTION (replaces Twilio WhatsApp)
def send_telegram_news():
    api_key = os.getenv("NEWS_API_KEY")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    subs = Subscription.objects.all()

    for sub in subs:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}&pageSize=3"

        response = requests.get(url).json()

        if not response.get("articles"):
            print("No articles found.")
            continue

        articles = response['articles']
        msg = f"📰 Top 3 {sub.category} News:\n\n" + "\n\n".join(
            f"{i+1}. {a['title']}" for i, a in enumerate(articles)
        )

        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': sub.chat_id,
            'text': msg
        }
        res = requests.post(send_url, data=payload)
        print(f"✅ Sent to {sub.name} ({sub.chat_id}) - status: {res.status_code}")




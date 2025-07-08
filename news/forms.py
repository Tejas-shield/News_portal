from django import forms
from .models import Comment, Subscription

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'chat_id']  # include chat_id

        widgets = {
            'chat_id': forms.TextInput(attrs={
                'placeholder': 'Enter your Telegram Chat ID',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
            }),
        }

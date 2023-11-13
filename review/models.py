from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CompanyProfile, UserProfile


User = get_user_model()


class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comment_ratings', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body} - {self.user}'


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='ratings_received', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')

    def __str__(self):
        return f'{self.rating} - {self.user}'


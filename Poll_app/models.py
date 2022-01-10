from django.db import models
from django.utils import timezone
from users.models import Profile
from django.conf import settings

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, default=4)
    def __str__(self):
        return f'{self.name}'

class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, default=4)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def __str__(self):
        return f'{self.question}'
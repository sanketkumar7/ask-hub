from django.db import models
from django.contrib.auth.models import AbstractUser
from .static_files import QUESTION_CATEGORIES
from datetime import datetime
# Create your models here.
class User(AbstractUser):
    phone_no=models.CharField(max_length=15)

class Question(models.Model):
    question=models.CharField(max_length=255)
    author=models.CharField(max_length=255)  #users username
    category=models.CharField(choices=QUESTION_CATEGORIES)
    created=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.question
    

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=1000)
    author=models.CharField(max_length=50) #users username
    likes=models.PositiveIntegerField(default=0)
    created=models.DateTimeField(default=datetime.now())
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)

    def  __str__(self):
        return f'answer id:{self.answer.id} liked by '+self.user.username


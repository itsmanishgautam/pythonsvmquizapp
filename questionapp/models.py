from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User  = get_user_model()
# Create your models here.
class Question(models.Model): 
    CATEGORY_CHOICES = [('HARD', 'HARD'),('EASY','EASY'),('UNCATEGORIZED','UNCATEGORIZED')]    
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,blank=True,null=True,default="UNCATEGORIZED")
    question = models.TextField()
    marks = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null=True,)
    updated = models.DateTimeField(default=timezone.now,null=True,) 
    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer = models.CharField(max_length=300)
    is_right = models.BooleanField(default=False)
    def __str__(self):
        return self.answer
    


class Test(models.Model):
    title = models.CharField(max_length=100,null=True,)
    questions = models.ManyToManyField(Question,related_name="tests",blank=True)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True,)
    updated = models.DateTimeField(default=timezone.now,null=True,)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title

class TestAttempt(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,)
    
    def __str__(self):
        return f"{self.user} - {self.test}"
    

class UserQuestionAttempt(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    test_attempt = models.ForeignKey(TestAttempt,on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='userquestionattempts')
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)
    time_taken = models.PositiveIntegerField(default=0) # in seconds
    right_attempt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -> {self.right_attempt} -> {self.answer}"

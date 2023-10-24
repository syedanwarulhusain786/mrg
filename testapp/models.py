from django.db import models

# Create your models here.


from django.db import models
# models.py
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Address Fields
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Payment by {self.user.username} on {self.payment_date}"
    
    
    
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    
class DownloadItem(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the title of the download item")
    file = models.FileField(upload_to='downloadsPage/', help_text="Choose a file to upload")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Download Item"
        verbose_name_plural = "Download Items"

class Video_Ea(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the title of the video")
    youtube_url = models.URLField(help_text="Enter the YouTube video URL")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        
        
class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"
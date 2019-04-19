from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image

# Create your models here.


class University(models.Model):
    public = 'Public'
    private = 'Private'
    eng_college = 'Engineering College'
    med_college = 'Medical College'
    type_choice = ((public, 'Public University'),
                   (private, 'Private University'),
                   (eng_college, 'Engineering College'),
                   (med_college, 'Medical College'))
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    content = models.TextField(default="")
    university_type = models.CharField(max_length=20, choices=type_choice, default=None)
    logo = models.ImageField(default='default.jpg', upload_to='uni_logo')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('university-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(University, self).save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)

class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})


class AdmissionNews(models.Model):
    title = models.CharField(max_length=512, default='')
    news = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('admissionnews-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(AdmissionNews, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    date_commented = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('admissionnews-detail', kwargs={'pk': self.post.pk})


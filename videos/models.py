from django.db import models
from sqlalchemy import true
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
import re
import datetime
import pytest
# Create your models here.
# class Video(models.Model):
#   title = models.CharField(max_length=255)
#   category = models.ForeignKey('Category',on_delete=models.SET_NULL, null=True)
#   youtube_link = models.URLField(max_length=255)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)
#   def __str__(self):
#     return self.title



def validate_subtitle(value):
    match = re.search(r"^\[\{('text': '[^{}]+', )?'attributes': \{'dur': '[0-9\.]+', 'start': '[0-9\.]+'\}\}, (\{('text': '[^{}]+', )?'attributes': \{'dur': '[0-9\.]+', 'start': '[0-9\.]+'\}\}, )*\{('text': '[^{}]+', )?'attributes': \{'dur': '[0-9\.]+', 'start': '[0-9\.]+'\}\}\]$", str(value))
    if not match:
        raise ValidationError(
            _('subtitle field is invalid format'),
            params={'value': value},
        )

def validate_thumbnails(value):
    match = re.search(r"^\[\{'url': '[^{}]+', 'width': [0-9\.]+, 'height': [0-9\.]+\}, (\{'url': '[^{}]+', 'width': [0-9\.]+, 'height': [0-9\.]+\}, )*\{'url': '[^{}]+', 'width': [0-9\.]+, 'height': [0-9\.]+\}\]$", str(value))
    if not match:
        raise ValidationError(
            _('thumbnails field is invalid format'),
            params={'value': value},
        )


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    channel = models.ForeignKey('Channel', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1024)
    length_seconds = models.PositiveIntegerField(null=True)
    thumbnails = models.JSONField(validators=[validate_thumbnails], null=True)
    publish_date = models.DateField(null=True)
    subtitle = models.JSONField(null=True, validators=[validate_subtitle])
    is_outstanding = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      title = self.title
      title = removePunctuation(title)
      title = customSplit(title)
      print(title)
      for word in title:
        word_lower = word.lower()
        keyword = TitleInvertedIndex.objects.get(pk=word_lower)
        keyword.remove_video(self.id)
      super().delete(*args, **kwargs)


def removePunctuation(text):
    for ch in ['/',':','\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','?',',','"','&', "'"]:
        if ch in text:
            if (ch != '\''):
                text = text.replace(ch,' ')
            else:
                text = text.replace(ch, '')
    return text.strip()

def customSplit(text):
    text=text.split(' ')
    return [a for a in text if a != '']


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
      return self.name

class Channel(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=1024)
    profile_url = models.CharField(max_length=1024)
    thumbnail = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
      return self.name


class VideoInvertedIndex(models.Model):
  keyword = models.CharField(max_length=255, primary_key=True)
  videos = models.ManyToManyField(Video, related_name="keyword_in_videos")
  def __str__(self):
    return self.keyword

  def add_video(self, video_id):
        self.videos.add(video_id)

  def check_is_contain(self, video_id):
    try:
        self.videos.get(pk = video_id)
        return True
    except:
        return False

class TitleInvertedIndex(models.Model):
  keyword = models.CharField(max_length=255, primary_key=True)
  videosTitle = ArrayField(models.CharField(max_length=255))
  videosId = ArrayField(models.CharField(max_length=255))
  def __str__(self):
    return self.keyword

  def add_video(self, title, id):
    self.videosTitle.append(title)
    self.videosId.append(id)
    self.save()

  def remove_video(self, id):
    for i in range(len(self.videosId)):
      if self.videosId[i] == id:
        self.videosId.pop(i)
        self.videosTitle.pop(i)
        break
    self.save()



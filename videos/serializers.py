from rest_framework import serializers
from .models import Video,Category

class GetAllVideosSerializer(serializers.ModelSerializer):
  class Meta:
    model = Video 
    fields = [
            'id',
            'category',
            'channel',
            'title',
            'length_seconds',
            'thumbnails',
            'publish_date',
            'is_outstanding',
        ]

class GetAllCategoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Category 
    fields = ['id','name']


class VideoCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Video 
    fields = ['id','title','category', 'youtube_link']

  def save(self):
    try:
      title = self.validated_data['title']
      category=self.validated_data['category']
      youtube_link=self.validated_data['youtube_link']
      video = Video(
        title=title, category=category, youtube_link=youtube_link
      )
      video.save()
      return video
    except KeyError:
      raise serializers.ValidationError({"response": "Data is not correct"})


class SearchVideoBodySerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1,allow_null=False, required=False)
    title = serializers.CharField(allow_null=True)
from rest_framework import mixins
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.http import HttpResponseNotFound
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# from videos.pagination import CustomPagination
from .serializers import GetAllVideosSerializer,GetAllCategoriesSerializer, SearchVideoBodySerializer,VideoCreateSerializer
from .models import Video, Category, VideoInvertedIndex, TitleInvertedIndex, removePunctuation, customSplit
from django.core.exceptions import ObjectDoesNotExist
import pytest
import re
import math
from datetime import datetime
from django.conf import settings


def check_string_only_number(string):
  regex = '^[0-9]+$'
  if(re.search(regex, string)):
      return True
  else:
      return False

def index(request):
  return render(request, 'index.html')

def filterVideosByTitle(videos, keyword):
  result = []
  arrKw = keyword.split(' ')
  if (len(arrKw) == 1):
    return  videos.filter(title__contains=keyword)
  else:
    # for video in videos: # lap n lan, voi n la so luong video
    #   flag = True 
    #   for kw in arrKw: # lap m lan, voi m la so luong words cua title
    #     if kw not in video.title: # lap k lan, voi k la so luong characters cua video.title
    #       flag = False
    #       continue
    #   if (flag):
    #     result.append(video)
    for kw in arrKw: 
      videos = videos.filter(title__contains=kw)


  print("result:", result)
  return (videos)
  # return result
  # O(n x m x k)
    


class VideoListView(APIView):
  def get(self, request):
    videos = Video.objects.select_related('category')
    title = self.request.query_params.get('title')
    category = self.request.query_params.get('category')
    # print(title.split(' '))
    if title is None:
      print('hello')
    if title is not None and category is not None:
      videos = videos.filter(title__contains=title, category__id=category)
    elif title is not None:
      videos = filterVideosByTitle(videos, title)
      # videos = videos.filter(title__contains=title)
    elif category is not None:
      videos = videos.filter(category__id=category)
    print("h2: ",videos)
    serializer = GetAllVideosSerializer(videos, many=True)
    return Response(serializer.data)
    

class VideoDetailView(APIView):
  http_method_names = [
        'delete',
        'get',
    ]

  def get_object(self, pk):
      try:
          return Video.objects.get(pk=pk)
      except Video.DoesNotExist:
          raise Http404

  def get(self, request, pk, format=None):
      snippet = self.get_object(pk)
      serializer = GetAllVideosSerializer(snippet)
      return Response(serializer.data)

  def delete(self, requset, pk, format=None):
    print("pk",pk)
    snippet = self.get_object(pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


  # def post(self, request):
  #   data = request.data
  #   serializer = VideoCreateSerializer(data=data)
  #   data = {}
  #   if serializer.is_valid():
  #     video = serializer.save()
  #     data['title'] = video.title
  #     data['category_name'] = video.category.name
  #     data['youtube_link'] = video.youtube_link
  #     return Response(data=data, status=status.HTTP_200_OK)


class CategoryListView(APIView):
  def get(self, request):
    try:
      categories = Category.objects.all()
    except Category.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
      serializer = GetAllCategoriesSerializer(categories, many=True)
      return Response(serializer.data)


from django.contrib.postgres.search import SearchQuery, SearchVector

class TextSearchView(APIView):
  def get(self, request):
    titleQuery = self.request.query_params.get('title')

    videos = Video.objects.filter(title__search="python")

    serializer = GetAllVideosSerializer(videos, many=True)
    return Response(serializer.data)



# from rapidfuzz import fuzz, process

# class TextSearchView(APIView):
#   def get(self, request):
#     videos = Video.objects.select_related('category')
#     title = self.request.query_params.get('title')
#     titleArray = list(videos.values_list('title', flat=True))
#     print(titleArray)
#     # choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys","New York Giants 222"]
#     resultIndexes = process.extract(title, titleArray, scorer=fuzz.WRatio, score_cutoff=50)
#     print(resultIndexes)
#     # pytest.set_trace()
#     result = []
#     for r in resultIndexes:
#       result.append(videos[r[2]])
#     serializer = GetAllVideosSerializer(result, many=True)
#     return Response(serializer.data)



import nltk
from collections import OrderedDict, defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# def removePunctuation(text):
#     for ch in ['/',':','\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','?',',','"','&', "'"]:
#         if ch in text:
#             if (ch != '\''):
#                 text = text.replace(ch,' ')
#             else:
#                 text = text.replace(ch, '')
#     return text.strip()

# def customSplit(text):
#     text=text.split(' ')
#     return [a for a in text if a != '']

class InvertedIndexView(APIView):
  def get(self, request):
    now = datetime.now()
    print("Current Time =", now)

    count_repeat = defaultdict(int)
    title = self.request.query_params.get('title')
    title = removePunctuation(title)
    title = customSplit(title)
    stwords = set(stopwords.words('english'))
    stwords.remove('you')

    
    arrTitle = []
    # for sent in sent_tokenize(title):
    #     for word in word_tokenize(sent):
    #         word_lower = word.lower()
    #         if word_lower not in stwords:
    #           arrTitle.append(word_lower)

    for word in title:
      word_lower = word.lower()
      if word_lower not in stwords:
        arrTitle.append(word_lower)
    print(arrTitle)
    
    for kw in arrTitle:  
        queryset = VideoInvertedIndex.objects.get(pk=kw).videos.all() # queryset video
        # querysetArr = list(queryset)
        now = datetime.now()
        print("Current Time 2 =", now)
        for item in queryset:
            print("type: ", type(item))
            if count_repeat[item] is None:
                count_repeat[item] = 1
            else:
                count_repeat[item] += 1 
    # pytest.set_trace()
    sortedCountArray = dict(sorted(count_repeat.items(), key=lambda x: (x[1], len(x[0].title)*(-1)), reverse=True))
    # sortedCountArray = dict(sorted(count_repeat.items(), key=lambda x: (x[1]), reverse=True))
    print(len(sortedCountArray))
    serializer = GetAllVideosSerializer(sortedCountArray.keys(), many=True)
    # serializer = GetAllVideosSerializer([], many=True)
    now = datetime.now()
    print("Current Time end func =", now)
    return Response(serializer.data)



  def post(self, request):
    videos = Video.objects.all()
    videoArray = map(lambda x: {"id": x.id, "title": x.title},list(videos))
    count = 0
    for item in (videoArray):
        title = removePunctuation(item['title'])
        title = customSplit(title)
        count += 1
        print(count)
        for word in title:
            word_lower = word.lower()
            video_id = item['id']
            try:
              keyword = VideoInvertedIndex.objects.get(pk=word_lower) # neu ton tai key word
              if (keyword.check_is_contain(video_id) == False):
                  keyword.add_video(video_id)
            except:
              # VideoInvertedIndex(keyword = word_lower).save()
              keyword = VideoInvertedIndex.objects.create(keyword = word_lower)
              keyword.add_video(video_id)


    return Response("successfully")



  def put(self, request):
    videos = Video.objects.all()
    videoArray = map(lambda x: {"id": x.id, "title": x.title},list(videos))
    for item in (videoArray):
            for word in item['title'].split(' '):
                word_lower = word.lower()
                try:
                    video_id = item['id']
                    keyword = VideoInvertedIndex.objects.get(pk=word_lower)
                    if (keyword.check_is_contain(video_id) == False):
                        keyword.add_video(video_id)
                except:
                    print("falsy")
    return Response("successfully")




class TitleInvertedIndexView(APIView):
  def get(self, request):
    PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']
    title = self.request.query_params.get('title')
    page = self.request.query_params.get('page')
    if (page is None):
      page = 1

    print("title:", title)
    body = SearchVideoBodySerializer(data={
      "title": title,
      "page": page
    })
    if body.is_valid() is False:
        return Response({"detail": "Invalid page."}, status = status.HTTP_404_NOT_FOUND)
    
    if title is None:
      queryset = Video.objects.all()
      count= queryset.count()
      MAX_PAGE = math.ceil(count/PAGE_SIZE)
      print(MAX_PAGE)
      page = body.validated_data["page"]
    
      if (page > MAX_PAGE or page < 0):
        return Response({"detail": "Invalid page."}, status = status.HTTP_404_NOT_FOUND)

      sliceObj = slice(PAGE_SIZE*(page-1), PAGE_SIZE*(page))
      queryset = queryset[sliceObj]
      videos = GetAllVideosSerializer(queryset, many=True)
    
      return Response(OrderedDict([
        ('count', count),
        ('next', None),
        ('previous', None),
        ('results', videos.data)
      ]))

    concatString = '&&(^-^)&&'
    count_repeat = defaultdict(int)
    title = removePunctuation(title)
    title = customSplit(title)
    stwords = set(stopwords.words('english'))
    stwords.remove('you')
    arrTitle = []
    
    for word in title:
      word_lower = word.lower()
      if word_lower not in stwords:
        arrTitle.append(word_lower)
    for kw in arrTitle:  
        try: 
          queryset = TitleInvertedIndex.objects.get(pk=kw) # queryset video
          listTitles = queryset.videosTitle
          listIds = queryset.videosId
        except:
          continue
        for i in range(len(listTitles)):
            key = listTitles[i] + concatString + listIds[i]
            if count_repeat[key] == 0:
                count_repeat[key] = 1
            else:
                count_repeat[key] += 1 
    if len(count_repeat) == 0:
      return Response(OrderedDict([
      ('count', 0),
      ('next', None),
      ('previous', None),
      ('results', [])
    ]))
    sortedCountArray = dict(sorted(count_repeat.items(), key=lambda x: (x[1], len(x[0].split(concatString)[0])*(-1)), reverse=True))
    arrayId = []
    for i in sortedCountArray.keys():
        arrayId.append(i.split(concatString)[1])
    
    MAX_PAGE = math.ceil(len(sortedCountArray)/PAGE_SIZE)
    page = body.validated_data["page"]
  
    
    if (page > MAX_PAGE or page < 0):
      return Response({"detail": "Invalid page."}, status = status.HTTP_404_NOT_FOUND)

    sliceObj = slice(PAGE_SIZE*(page-1), PAGE_SIZE*(page))
    arrayId = arrayId[sliceObj]
    queryset = []
    for i in arrayId:
        queryset.append(Video.objects.get(id=i))
    queryset = GetAllVideosSerializer(queryset, many=True)
    
    return Response(OrderedDict([
      ('count', len(sortedCountArray)),
      ('next', None),
      ('previous', None),
      ('results', queryset.data)
    ]))


  def post(self, request):
    videos = Video.objects.all()
    videoArray = map(lambda x: {"id": x.id, "title": x.title},list(videos))
    count = 0
    for item in (videoArray):
        title = removePunctuation(item['title'])
        title = customSplit(title)
        count += 1
        print(count)
        for word in title:
          word_lower = word.lower()
          try: # da co keyword
              video_id = item['id']
              keyword = TitleInvertedIndex.objects.get(pk=word_lower) 
              if (keyword.videosId.count(video_id) == 0):
                keyword.add_video(item['title'], item['id'])
          except: # chua co keyword
              keyword = TitleInvertedIndex.objects.create(keyword = word_lower, videosId= [], videosTitle=[])
              keyword.add_video(item['title'], item['id'])


    return Response("successfully")



  def put(self, request):
    id = self.request.query_params.get('id')
    print(id)
    video = Video.objects.get(pk=id)
    print(video.title)
    title = removePunctuation(video.title)
    title = customSplit(title)
    for word in title:
        word_lower = word.lower()
        try: # da co keyword
            video_id = video.id
            keyword = TitleInvertedIndex.objects.get(pk=word_lower) 
            if (keyword.videosId.count(video_id) == 0):
              keyword.add_video(video.title, video.id)
        except: # chua co keyword
            keyword = TitleInvertedIndex.objects.create(keyword = word_lower, videosId= [], videosTitle=[])
            keyword.add_video(video.title, video.id)
    return Response("successfully")






    




  



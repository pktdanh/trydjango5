import json
from rest_framework import status
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestVideoListView:
    client = APIClient()

    # def test_get_video_list(self, video1):
    #   # when
    #   assert  1==1
    #   # response = self.client.get('/video/')
    #   # # then
    #   # assert response.status_code == status.HTTP_200_OK
    #   # data = json.loads(response.content)
    #   # assert len(data) == 2

    def test_get_video_list(self, category):
      # when
      # assert  1==1
      response = self.client.get('/category/')
      # then
      assert response.status_code == status.HTTP_200_OK
      data = json.loads(response.content)
      # assert len(data) == 1
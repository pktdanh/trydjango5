from model_bakery.recipe import Recipe, foreign_key
from videos.models import Category, Video

category = Recipe(Category, name='a bc')
video1 = Recipe(Video, category=foreign_key(category), title='a', youtube_link='https://a.com/b')
video2 = Recipe(Video, category=foreign_key(category), title='a', youtube_link='https://a.com/c')



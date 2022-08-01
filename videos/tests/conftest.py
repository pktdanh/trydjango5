from model_bakery import baker
import pytest

@pytest.fixture
def video1():
    return baker.make_recipe("videos.tests.video1")

@pytest.fixture
def video2():
    return baker.make_recipe("videos.tests.video2")


@pytest.fixture
def category():
    return baker.make_recipe("videos.tests.category")

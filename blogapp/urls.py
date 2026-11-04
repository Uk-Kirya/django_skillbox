from django.urls import path
from .views import BlogListView, ArticleDetailView, LatestArticlesView

app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name="blog"),
    path('<int:pk>/', ArticleDetailView.as_view(), name="article"),
    path('latest/feed/', LatestArticlesView(), name="latest_articles"),
]

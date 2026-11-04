from django.contrib.syndication.views import Feed
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy

from blogapp.models import Article


class BlogListView(ListView):
    template_name = 'blogapp/index.html'
    model = Article
    queryset = (
        Article.objects
        .select_related('author', 'category')
        .prefetch_related('tags')
        .defer('content')
        .filter(pub_date__isnull=False)
        .order_by('-pub_date')
        .all()
    )
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    template_name = 'blogapp/article_detail.html'
    model = Article


class LatestArticlesView(Feed):
    title = 'Свежие статьи'
    description = 'Тут самые свежие статьи блога'
    link = reverse_lazy('blogapp:blog')

    def items(self):
        return (
            Article.objects
            .select_related('author', 'category')
            .prefetch_related('tags')
            .defer('content')
            .filter(pub_date__isnull=False)
            .order_by('-pub_date')
            .all()[:2]
        )

    def item_title(self, item: Article) -> str:
        return item.title

    def item_description(self, item: Article) -> str:
        return item.content[:100]

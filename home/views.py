from django.views.generic import TemplateView

from shopapp.models import Product


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products"] = Product.objects.defer('created_at', 'archived', 'test', 'availability', 'description').all()[:4]

        return context


class AboutView(TemplateView):
    template_name = "home/about.html"


class ContactView(TemplateView):
    template_name = "home/contacts.html"

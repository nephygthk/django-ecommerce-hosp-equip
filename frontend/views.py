from django.shortcuts import render
from django.views.generic import TemplateView

from store.models import Product

class HomeView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
       context = super(HomeView, self).get_context_data(**kwargs)
       context['products'] = Product.objects.all()
       context['featured_products'] = context['products'].filter(is_featured=True)
       return context


class AboutView(TemplateView):
    template_name = 'frontend/about.html'


class ContactView(TemplateView):
    template_name = 'frontend/contact.html'
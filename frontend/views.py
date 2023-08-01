from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.core.mail import send_mail

from store.models import Product

class HomeView(TemplateView):
    template_name = 'frontend/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponseRedirect(reverse_lazy('account:admin_dashboard'))
            else:
                return HttpResponseRedirect(reverse_lazy('account:patient_dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
       context = super(HomeView, self).get_context_data(**kwargs)
       context['products'] = Product.objects.all()
       context['featured_products'] = context['products'].filter(is_featured=True)
       return context


class AboutView(TemplateView):
    template_name = 'frontend/about.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponseRedirect(reverse_lazy('account:admin_dashboard'))
            else:
                return HttpResponseRedirect(reverse_lazy('account:patient_dashboard'))
        return super().dispatch(request, *args, **kwargs)


class ContactView(TemplateView):
    template_name = 'frontend/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # f_message = render_to_string()

        try:
            send_mail(
                'Message From '+name+' <'+email+'>',
                message,
                'contact@clevelandmedcenter.org',
                ['contact@clevelandmedcenter.org'],
                fail_silently=False,
            )
            messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
        except:
            messages.error(request, 'There was an error while trying to send your email, please try again')

        finally:
            return HttpResponseRedirect(reverse_lazy('frontend:contact'))


class AllProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'frontend/products.html'
    paginate_by = 20


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'frontend/product_detail.html'
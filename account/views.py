from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView

from .models import Customer
from account.forms import RegistrationForm, UserLoginForm 
from store.models import Product
from store.forms import AddProductForm, MediaFormSet 
from orders.models import Order



class RegisterUserView(FormView):
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('account:login')
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        messages.success(self.request, "Your account was created successfully, please login below")
        return super(RegisterUserView, self).form_valid(form)
    
    
def user_index_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('account:admin_dashboard')
            else:
                return redirect('account:customer_dashboard')
        else:
            messages.error(request, 'Invalid login cridentials, check and try again')
            return redirect('frontend:home')


class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = 'account/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('account:admin_dashboard')
        else:
            return reverse_lazy('account:customer_dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid Email or password, please try again')
        return self.render_to_response(self.get_context_data(form=form))


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super(AdminDashboardView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:8]
        context['customers'] = Customer.objects.filter(is_staff=False)[:8]
        context['orders'] = Order.objects.all()
        return context


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/customer_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)


class AddProductView(LoginRequiredMixin, CreateView):
   form_class = AddProductForm
   model = Product
   template_name = "store/product_create_or_update.html"
   success_url = reverse_lazy('account:admin_dashboard')

   def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponse("Error handler content", status=400)
        return super().dispatch(request, *args, **kwargs)

   def form_valid(self, form):
      ctx = self.get_context_data()
      media_form = ctx['media_form']
      
      if media_form.is_valid() and form.is_valid():      
         prod = form.save()
         media_form.instance = prod
         media_form.save()
         messages.success(self.request, 'Product was added successfully')
      return super(AddProductView, self).form_valid(form)

   def get_context_data(self, **kwargs):
      ctx = super(AddProductView,self).get_context_data(**kwargs)
      ctx['title'] = 'Add New Product'
      if self.request.POST:
         ctx['form']= AddProductForm(self.request.POST)
         ctx['media_form']= MediaFormSet(self.request.POST, self.request.FILES)
      else:
         ctx['form']= AddProductForm()
         ctx['media_form']= MediaFormSet()
      return ctx


@login_required(login_url='account:login')
def delete_product(request, pk):
    if not request.user.is_staff:
        return HttpResponse("Error handler content", status=400)
    product = Product.objects.get(pk=pk)
    product.delete()
    messages.success(request, 'product was deleted successfully')
    return redirect('account:admin_dashboard')


@login_required(login_url='account:login')
def delete_customer(request, pk):
    if not request.user.is_staff:
        return HttpResponse("Error handler content", status=400)
    customer = Customer.objects.get(pk=pk)
    customer.delete()
    messages.success(request, 'Customer was deleted successfully')
    return redirect('account:admin_dashboard')
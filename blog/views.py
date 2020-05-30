from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Post, Zahtjev
from users.models import User, Donator
from django.http import JsonResponse
from django.urls import reverse
import stripe
from users.models import Profile


# Create your views here.


stripe.api_key = "sk_test_sPrD7RKSpmQ7QSjFxwYU9r3x007aHGgUvp"

def home(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def zahtjev(request):
    context={
        'zahtjevi': Zahtjev.objects.all()
    }
    return render(request, 'blog/zahtjevi.html', context)


def hum_org(request):
    context = {
        'profili': Profile.objects.all().exclude(naziv="New User")

    }
    return render(request, 'blog/izbor_zahtjeva.html', context)


class OrgListView(ListView):
    model = Profile
    template_name = 'blog/izbor_zahtjeva.html'
    context_object_name = 'profili'
    ordering = ['naziv']




class ZahtjevListView(UserPassesTestMixin,ListView):
    model = Zahtjev
    template_name = 'blog/zahtjevi.html'
    context_object_name = 'zahtjevi'
    ordering = ['-date_posted']

    paginate_by = 5

    def test_func(self):
        #post = self.get_object()
        if(self.request.user.is_staff ):
            return True
        return False



def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

def mainhome(request):
    return render(request, 'blog/main_home.html', {'title': 'main'})


def charge(request,pk):
    amount = 5
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email = request.user.email,
            name = request.user.donator.full_name,
            source = request.POST['stripeToken'],
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='eur',
            description= Post.objects.get(pk=pk).title

        )
        a = Post.objects.get(pk=pk)
        a.povecaj(amount)
        a.save()




    return redirect(reverse('success', args=[amount]))

def successMsg(request, args):
    amount = args



    return render(request, 'blog/uspjesna_donacija.html', {'amount':amount})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class DetailListView(DetailView):
    model = Post

class DetailZahtjevView(DetailView):
    model = Zahtjev


class PostCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):

    model = Post
    fields = ['title', 'content', 'uplatni_racun', 'adresa', 'hitnost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        #post = self.get_object()

        if(self.request.user.autentifikacija):
            return True
        return False



class ZahtjevCreateView(LoginRequiredMixin, CreateView):

    model = Zahtjev
    fields = ['title', 'content', 'potrebna_sr']
    template_name = 'blog/zathjev_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.hum_org = User.objects.get(pk=self.kwargs.get('pk')).profile

        return super().form_valid(form)

"""
    def test_func(self):
        #post = self.get_object()
        if(self.request.user.autentifikacija):
            return True
        return False
"""

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'uplatni_racun', 'adresa', 'stanje', 'hitnost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if(self.request.user == post.author):
            return True
        return False

class ZahtjevUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zahtjev
    fields = ['title', 'content', 'potrebna_sr']
    template_name = 'blog/zathjev_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        zahtjev = self.get_object()
        if(self.request.user == zahtjev.author):
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if(self.request.user == post.author):
            return True
        return False
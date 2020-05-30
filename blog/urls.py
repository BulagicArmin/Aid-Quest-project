from django.urls import path
from .views import PostListView, DetailListView, PostCreateView, PostUpdateView, PostDeleteView,\
    UserPostListView, DetailZahtjevView, ZahtjevCreateView, ZahtjevUpdateView, ZahtjevListView,OrgListView
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    path('home/', PostListView.as_view(), name='blog-home'),
    path('user/<int:pk>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', DetailListView.as_view(), name='post-detail'),
    path('post/new/', staff_member_required(PostCreateView.as_view()), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/charge/', views.charge, name='charge'),
    path('success/<str:args>/', views.successMsg, name='success'),
    path('zahtjev/', ZahtjevListView.as_view(), name='zahtjev-home'),
    path('organizacije/', OrgListView.as_view(), name='organizacije'),
    path('zahtjev/<int:pk>/', DetailZahtjevView.as_view(), name='zahtjev-detail'),
    path('profile/<int:pk>/zahtjev/new/', ZahtjevCreateView.as_view(), name='zahtjev-create'),
    path('zahtjev/<int:pk>/update/', ZahtjevUpdateView.as_view(), name='zahtjev-update'),

    path('about/', views.about, name='blog-about'),
    path('', views.mainhome, name='main-home'),

]

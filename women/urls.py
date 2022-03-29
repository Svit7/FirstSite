from django.urls import path
# from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', AboutSite.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),

    # ajax
    path('comment_status/<int:pk>/<slug:type>', comment_status, name='update_comment_status')
]

# cache_page(60)(WomenHome.as_view())

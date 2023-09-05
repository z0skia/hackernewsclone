from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from hckrnews.views import signup
from story.views import home, submit, newest, vote, story


urlpatterns = [
    path('', home, name='home'),
    path('newest', newest, name='newest'),    
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='login.html', next_page=home), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('submit/', submit, name='submit'),
    path('s/<int:story_id>/vote/', vote, name='vote'),
    path('s/<int:story_id>/', story, name='story'),
    path('u/', include('userprofile.urls')),
]

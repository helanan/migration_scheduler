from django.urls import path

from . import views

app_name = 'dicalendar'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # ex: /dicalendar/5/, here is where you change the href url as well for each template
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /dicalendar/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # # ex: /dicalendar/5/vote
    path('<int:migration_id>/vote/', views.vote, name='vote'),
]

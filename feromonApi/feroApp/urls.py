from django.urls import path
from feroApp import views
#for function views
# urlpatterns = [
#     path('snippets/', views.snippet_list),
#     path('snippets/<int:pk>/', views.snippet_detail),
#     path('api/predict/', views.api_sentiment_pred, name='api_sentiment_pred'), 
# ]

urlpatterns = [
    path('feromon/predict/', views.feromon_view, name='feromon_view'),
    path('feromon/jsontogeo/', views.jsontogeojson, name='jsontogeojson'),
    path('feromon/geojsontojson/', views.geojsontojson, name='geojsontojson'),
]

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns,allowed=['json', 'html'])
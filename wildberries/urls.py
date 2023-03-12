from django.urls import path

from wildberries.views import CardView

urlpatterns = [
    path('card/', CardView.as_view({'post': 'post'}), name='card'),
]

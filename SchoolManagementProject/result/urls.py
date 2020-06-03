from django.urls import path
from .views import *

urlpatterns = [
    path('create/',create_result,name='create-result'),
    path('edit-result/',edit_result,name='edit-results'),
    path('view/all',all_results_view,name='view-results'),
]

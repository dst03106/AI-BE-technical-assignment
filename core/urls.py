from django.urls import re_path
from .views import get_talent_experiences

urlpatterns = [
    # ... existing URL patterns ...
    re_path("v1/talent-experiences/?$", get_talent_experiences, name="get_talent_experiences"),
]

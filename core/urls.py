from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from custom_user.urls import router

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('obtain-api-token/', obtain_jwt_token),
]

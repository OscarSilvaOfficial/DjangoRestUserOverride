from rest_framework import routers
from custom_user import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
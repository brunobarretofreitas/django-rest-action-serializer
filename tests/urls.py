from rest_framework.routers import DefaultRouter

from .viewsets import UserModelViewSet, UserNoActionConfigModelViewSet

router = DefaultRouter()
router.register(r'users', UserModelViewSet, basename='user')
router.register(
    r'users-no-action-config',
    UserNoActionConfigModelViewSet,
    basename='user-no-action-config'
)

urlpatterns = router.urls
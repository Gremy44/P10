"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from API.views import ProjectViewset, ContributorsViewset,\
    IssueViewset, CommentViewset
from authentication.views import SignupViewset, UsersViewset, ActualUserView

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,\
    TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="SoftDesc API",
        default_version='v1',
        description="SoftDesc api swagger",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def redirect_to_swagger(request):
    return redirect('/swagger/')


router = routers.SimpleRouter()

router.register(r'auth/getuser', UsersViewset, basename='getuser')
router.register(r'auth/actual-user', ActualUserView, basename='actual-user')
router.register(r'auth/signup', SignupViewset, basename='signup')

'''
generates:
 /projects/
 /projects/{pk}/
'''
router.register(r'projects', ProjectViewset, basename='project')

'''
generates:
 /projects/{project_pk}/users/
 /projects/{project_pk}/users/{pk}/
'''
contributor_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
contributor_router.register(r'users', ContributorsViewset, basename='user')

'''
generates:
 /projects/{project_pk}/issues/
 /projects/{project_pk}/issues/{pk}/
'''
issue_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
issue_router.register(r'issues', IssueViewset, basename='issue')

'''
generates:
 /projects/{project_pk}/issues{issue_pk}/comments
 /projects/{project_pk}/issues{issue_pk}/comments/{pk}/
'''
comment_router = routers.NestedSimpleRouter(
    issue_router, r'issues', lookup='issue')
comment_router.register(r'comments', CommentViewset, basename='comment')

urlpatterns = [
    path('', redirect_to_swagger),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path(r'admin/', admin.site.urls),
    path(r'api/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(r'api/auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path(r'api/', include(router.urls)),
    path(r'api/', include(contributor_router.urls)),
    path(r'api/', include(issue_router.urls)),
    path(r'api/', include(comment_router.urls)),
]

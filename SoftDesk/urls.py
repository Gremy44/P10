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
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from API.views import ProjectViewset, ContributorsViewset, IssueViewset, CommentViewset
from authentication.views import SignupViewset, UsersViewset, ActualUserView

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()

router.register(r'auth/getuser', UsersViewset, basename='getuser')
router.register(r'auth/actual-user', ActualUserView, basename='actual-user')
router.register(r'auth/signup', SignupViewset, basename='signup')

'''
generates:
 /projects/
 /projects/{pk}/
'''
router.register(r'projects', ProjectViewset, basename='projects')

'''
generates:
 /projects/{project_pk}/users/
 /projects/{project_pk}/users/{pk}/
'''
contributor_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
contributor_router.register(r'users', ContributorsViewset, basename='users')

'''
generates:
 /projects/{project_pk}/issues/
 /projects/{project_pk}/issues/{pk}/
'''
issue_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
issue_router.register(r'issues', IssueViewset, basename='issues')

'''
generates:
 /projects/{project_pk}/issues{issue_pk}/comments
 /projects/{project_pk}/issues{issue_pk}/comments/{pk}/
'''
comment_router = routers.NestedSimpleRouter(issue_router, r'issues', lookup='issue')
comment_router.register(r'comments', CommentViewset, basename='comments')

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'api/', include(router.urls)),
    path(r'api/', include(contributor_router.urls)),
    path(r'api/', include(issue_router.urls)),
    path(r'api/', include(comment_router.urls)),
]

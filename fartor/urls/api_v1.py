from django.urls import path

from fartor.apps.accounting.users.actions.login import LoginRestAPI
from fartor.apps.accounting.users.actions.self import SelfRestAPI

urlpatterns = [
    # user login
    path('auth/login/', LoginRestAPI.as_view()),
    path('auth/self/', SelfRestAPI.as_view()),
]

# from django.contrib import admin
from django.urls import path
from dashboard import views
app_name = 'dashboard'
urlpatterns = [
    # path('dashboard/', ),
    path("",views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('signup/',views.signupPage,name='signup'),
    path('take_test/',views.test_index,name='take_test_index'),
    path('take_test/<int:test_id>/',views.testPage,name='taketest'),
    path('questionpool/',views.list_questions,name='questionpool'),
    path('add_option/<int:question_id>/',views.add_option,name='add_option'),
    path('list_test/',views.list_test,name='list_test'),
    path('add_test/',views.add_test,name='add_test'),

]   
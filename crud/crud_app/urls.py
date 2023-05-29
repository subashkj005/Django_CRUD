from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='userlogin'),
    path('adminlogin', views.admin_login, name='adminLogin'),
    path('adminHome', views.admin_home, name='adminHome'),
    path('signup', views.signup, name='signup'),
    path('userHome', views.user_home, name='userHome'),
    path('logout', views.logout, name='logout'),
    path('addUser', views.add_user, name='addUser'),
    path('editUser<int:id>', views.edit_user, name='editUser'),
    path('updateData<int:id>', views.update_data, name='updateData'),
    path('deleteUser<int:id>', views.delete_user, name='deleteUser'),

]
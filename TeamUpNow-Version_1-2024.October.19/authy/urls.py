from django.urls import path
from authy.views import profile, profile_saved, custom_login_view, signup, password_change, password_change_done, edit_profile, mentoring_follow

from django.contrib.auth import views as authViews 



urlpatterns = [
    path('profile/edit', edit_profile, name='edit-profile'),
   	path('signup/', signup, name='signup'),
	path('login/', custom_login_view, name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'stream'}, name='logout'),
   	path('changepassword/', password_change, name='change_password'),
   	path('changepassword/done', password_change_done, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]



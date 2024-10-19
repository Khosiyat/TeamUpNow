from django.urls import path
from notifications.views import display_notifications, delete_notification, count_notifications

urlpatterns = [
   	path('', display_notifications, name='show-notifications'),
   	path('<noti_id>/delete', delete_notification, name='delete-notification'),

]
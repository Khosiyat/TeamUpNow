from django.contrib import admin
from notifications.models import Notification, Notification_StartUp
# Register your models here.
admin.site.register(Notification)
admin.site.register(Notification_StartUp)

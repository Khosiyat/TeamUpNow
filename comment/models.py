from django.db import models

from post_StartUp.models import Post_StartUp
from post.models import Post 

from django.contrib.auth.models import User 
from notifications.models import Notification, Notification_StartUp

from django.db.models.signals import post_save, post_delete


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

 
class Comment(models.Model):
	COMMENT_CATEGORY = [
	('bug', 'bug'), 
	('solution', 'solution'),
	('question', 'question'),
	('feedback', 'feedback'),
]
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField(null=True,  blank=True)
	comment_category=models.TextField( null=False,  blank=False, choices=COMMENT_CATEGORY, default='bug') 
	bug_code =  models.URLField(max_length=200, null=True, blank=True, verbose_name='bug_code.com', default='github.com')
	date = models.DateTimeField(auto_now_add=True)

	def user_comment_post(sender, instance, *args, **kwargs):
		comment = instance
		post = comment.post
		text_preview = comment.body[:90]
		sender = comment.user
		notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
		notify.save()

	def user_del_comment_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
		notify.delete()

#Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)



class Comment_StartUp(models.Model):
	COMMENT_CATEGORY = [
	('solution', 'solution'),
	('question', 'question'),
	('feedback', 'feedback'),
]
	post = models.ForeignKey(Post_StartUp, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField(null=True,  blank=True)
	comment_category=models.TextField( null=False,  blank=False, choices=COMMENT_CATEGORY, default='bug') 
	bug_code =  models.URLField(max_length=200, null=True, blank=True, verbose_name='bug_code.com', default='github.com')
	date = models.DateTimeField(auto_now_add=True)

	def user_comment_post(sender, instance, *args, **kwargs):
		comment = instance
		post = comment.post
		text_preview = comment.body[:90]
		sender = comment.user
		notify = Notification_StartUp(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
		notify.save()

	def user_del_comment_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification_StartUp.objects.filter(post=post, sender=sender, notification_type=2)
		notify.delete()

#Comment
post_save.connect(Comment_StartUp.user_comment_post, sender=Comment_StartUp)
post_delete.connect(Comment_StartUp.user_del_comment_post, sender=Comment_StartUp)
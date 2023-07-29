import uuid
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

from notifications.models import Notification, Notification_StartUp


# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


 
class Tag_StartUp(models.Model):
	title = models.CharField(max_length=75, verbose_name='Tag_StartUp')
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='Tag_StartUp'
		verbose_name_plural = 'Tags_StartUp'

	def get_absolute_url(self):
		return reverse('tags_StartUp', args=[self.slug])
		
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)
 
 
class PostFileContent_StartUp(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner_StartUp')
	file = models.FileField(upload_to=user_directory_path)



class Post_StartUp(models.Model):
	CLASS_CATEGORY = [
	('Business Idea', 'Business Idea'), 
	('Business Plan', 'Business Plan'), 
	('Pitching', 'Pitching'), 
	('MVP/Idea Validation', 'MVP/Idea Validation'), 
	('Seed', 'Seed'), 
	('Series A', 'Series A'), 
	('Growth(Series B, C)', 'Growth(Series B, C)'), 
	('Scale(D+)', 'Scale(D+)'), 
	('Established expansion', 'Established expansion'), 
	('Maturity', 'Maturity'), 
	('Exit', 'Exit'), 
	('Marketing', 'Marketing'), 
	('(Co)Founders', '(Co)Founders'),
]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	content =  models.ManyToManyField(PostFileContent_StartUp, null=True, blank=True,  related_name='contents_StartUp')
	lessonLink = models.URLField(max_length=200, null=True, blank=True, verbose_name='youtube.com', default='youtube.com')
	codeSourceOfTheProject = models.URLField(max_length=200, null=True, blank=True, verbose_name='founderinstitute.com', default='founderinstitute.com')
	authorOfTheVideo =models.TextField(max_length=50, verbose_name='authorOfTheVideo', default='The author Of The Video')
	caption = models.TextField(max_length=1500, verbose_name='Caption_StartUp')
	classCategory = models.TextField( null=True,  blank=True, choices=CLASS_CATEGORY)
	posted = models.DateTimeField(auto_now_add=True)
	tagsStartUp = models.ManyToManyField(Tag_StartUp, related_name='tags_StartUp')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	illustrated = models.IntegerField(default=1)
	instructed = models.IntegerField(default=1)
 

	def get_absolute_url(self):
		return reverse('postdetails_StartUp', args=[str(self.id)])

	def __str__(self):
		return str(self.id)
 

 
class Instructed_StartUp(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_instructed_StartUp')
	post = models.ForeignKey(Post_StartUp, on_delete=models.CASCADE, related_name='post_instructed_StartUp')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification_StartUp(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification_StartUp.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()



class Illustrated_StartUp(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_illustrated_StartUp')
	post = models.ForeignKey(Post_StartUp, on_delete=models.CASCADE, related_name='post_illustrated_StartUp')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification_StartUp(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification_StartUp.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()
 
#Instructed_StartUp
post_save.connect(Instructed_StartUp.user_liked_post, sender=Instructed_StartUp)
post_delete.connect(Instructed_StartUp.user_unlike_post, sender=Instructed_StartUp)

#Illustrated_StartUp
post_save.connect(Illustrated_StartUp.user_liked_post, sender=Illustrated_StartUp)
post_delete.connect(Illustrated_StartUp.user_unlike_post, sender=Illustrated_StartUp)

 
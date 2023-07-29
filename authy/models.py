from django.db import models
from django.contrib.auth.models import User

from post_StartUp.models import Post_StartUp
from post.models import Post

from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

# Create your models here.
class Profile(models.Model):
	CLASS_CATEGORY = [
	('Language', 'Language'), 
	('Framework', 'Framework'),
	('Web Project', 'Web Project'),
	('Game Project', 'Game Project'),
	('Mobile Project', 'Mobile Project'),
	('AI Project', 'AI Project'),
	('Algorithms', 'Algorithms'),
	('Data Structures', 'Data Structures'),
	('Data Science', 'Data Science'),
	('Data Visualization', 'Data Visualization'),
	('Programming General', 'Programming General'),
]
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	first_name = models.CharField(max_length=50, null=False, blank=False, default='Team Member X')
	last_name = models.CharField(max_length=50, null=False, blank=False, default=' Y')
	location = models.CharField(max_length=50, null=False, blank=False, default='Location Z') 
	githubProfile = models.URLField(max_length=200, null=True, blank=True, verbose_name='githubProfile', default='github.com')
	linkedInnProfile = models.URLField(max_length=200, null=True, blank=True, verbose_name='linkedInnProfile', default='linkedin.com')
	interstCategory =models.TextField( null=False,  blank=False, choices=CLASS_CATEGORY, default='Programming General')
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	favorites_StartUp = models.ManyToManyField(Post_StartUp)
	picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		SIZE = 250, 250

		if self.picture:
			pic = Image.open(self.picture.path)
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)

	def __str__(self):
		return self.user.username
		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
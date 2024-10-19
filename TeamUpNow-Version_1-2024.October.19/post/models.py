import uuid
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

from notifications.models import Notification


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# class Tag(models.Model):
# 	title = models.CharField(max_length=75, verbose_name='Tag')
# 	slug = models.SlugField(null=False, unique=True)
# 	is_popular = models.BooleanField(default=False)

# 	class Meta:
# 		verbose_name='Tag'
# 		verbose_name_plural = 'Tags'

# 	def get_absolute_url(self):
# 		return reverse('tags', args=[self.slug])
		
# 	def __str__(self):
# 		return self.title

# 	def save(self, *args, **kwargs):
# 		if not self.slug:
# 			self.slug = slugify(self.title)
# 		return super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)
    is_popular = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        if self.slug:  # Ensure slug is not empty
            return reverse('tags', args=[self.slug])
        return '/'  # Return a default URL or handle the case appropriately

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title_post = models.CharField(max_length=100, null=False, blank=False, default="My Content")
	url_sourceContent = models.CharField(max_length=500, null=False, blank=False, default="TeamUpNow.tech")
	caption = models.TextField(max_length=500, verbose_name='Caption')
	posted = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, related_name='tags')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	interested = models.IntegerField(default=1)
	liked = models.IntegerField(default=1)
	


	def get_absolute_url(self):
		return reverse('post_details', args=[str(self.id)])

	def __str__(self):
		return str(self.id)

class Follow(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

	def user_follow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following
		notify = Notification(sender=sender, user=following, notification_type=3)
		notify.save()

	def user_unfollow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following

		notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
		notify.delete()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
    	post = instance
    	user = post.user
    	followers = Follow.objects.all().filter(following=user)
    	for follower in followers:
    		stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
    		stream.save()

class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()



class Liked(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_liked')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()



class Interested(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interested')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_interested')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()
 



#Stream
post_save.connect(Stream.add_post, sender=Post)

#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)


#liked
post_save.connect(Liked.user_liked_post, sender=Liked)
post_delete.connect(Liked.user_unlike_post, sender=Liked)

#interested
post_save.connect(Interested.user_liked_post, sender=Interested)
post_delete.connect(Interested.user_unlike_post, sender=Interested)


#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)
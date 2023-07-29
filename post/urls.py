from django.urls import path
from post.views import index, NewPost, PostDetails, tags, instructed, illustrated, favorite,pre_DeletePost, DeletePost, EditPost


urlpatterns = [
   	path('', index, name='index'),
   	path('newpost/', NewPost, name='newpost'), 
	
   	path('<uuid:post_id>', PostDetails, name='postdetails'),  

	path('<uuid:post_id>/instructed', instructed, name='post_instructed'),
	path('<uuid:post_id>/illustrated', illustrated, name='post_illustrated'), 

   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'), 
	
   	path('tag/<slug:tag_slug>', tags, name='tags'), 

	path('<uuid:event_id>/pre_DeletePost', pre_DeletePost, name='pre_DeletePost'), 
	path('<uuid:event_id>/DeletePost', DeletePost, name='DeletePost'),  

	path('<uuid:event_id>/EditPost', EditPost, name='EditPost'), 
]
from django.urls import path
from post.views import stream, post_details, tags, like, liked, interested, favorite, add_post, edit_post, delete_post, pre_delete_post


urlpatterns = [
   	path('', stream, name='stream'),
   	path('add_post/', add_post, name='add_post'),
   	path('<uuid:post_id>', post_details, name='post_details'),
   	path('<uuid:post_id>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
   	path('tag/<slug:tag_slug>', tags, name='tags'),
	path('<uuid:event_id>/EditPost', edit_post, name='edit_post'), 
	path('<uuid:event_id>/pre_delete_post', pre_delete_post, name='pre_delete_post'), 
	path('<uuid:event_id>/delete_post', delete_post, name='delete_post'),  
	path('<uuid:post_id>/liked', liked, name='post_liked'),
	path('<uuid:post_id>/interested', interested, name='post_interested'), 
	
]

from django.urls import path
from post_StartUp.views import  instructed_StartUp, illustrated_StartUp,favorite_StartUp, DeletePost_StartUp, pre_DeletePost_StartUp, NewPost_StartUp, PostDetails_StartUp, EditPost_StartUp,  tags_StartUp


urlpatterns = [ 
	path('newpost_StartUp/', NewPost_StartUp, name='newpost_StartUp'), 
	path('<uuid:post_id>', PostDetails_StartUp, name='postdetails_StartUp'), 

	path('<uuid:post_id>/instructed_StartUp', instructed_StartUp, name='post_instructed_StartUp'),
	path('<uuid:post_id>/illustrated_StartUp', illustrated_StartUp, name='post_illustrated_StartUp'), 
	path('<uuid:post_id>/favorite_StartUp', favorite_StartUp, name='postfavorite_StartUp'),
	path('tags_StartUp/<slug:tag_slug>', tags_StartUp, name='tags_StartUp'),  

	path('<uuid:event_id>/pre_DeletePost_StartUp', pre_DeletePost_StartUp, name='pre_DeletePost_StartUp'), 
	path('<uuid:event_id>/DeletePost_StartUp', DeletePost_StartUp, name='DeletePost_StartUp'), 
	path('<uuid:event_id>/EditPost_StartUp', EditPost_StartUp, name='EditPost_StartUp'), 
]
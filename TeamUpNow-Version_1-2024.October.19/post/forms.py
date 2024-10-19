from django import forms
from post.models import Post

from django.forms import ClearableFileInput

class NewPostForm(forms.ModelForm):
	title_post = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), required=True)
	url_sourceContent = forms.URLField(widget=forms.TextInput(attrs={'class': 'input is-small'}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-small'}), required=True)

	class Meta:
		model = Post
		fields = ('title_post', 'url_sourceContent', 'caption', 'tags')
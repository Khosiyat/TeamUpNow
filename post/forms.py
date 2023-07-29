from django import forms
from post.models import Post 

from django.forms import ClearableFileInput

class NewPostForm(forms.ModelForm):
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

	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	lessonLink= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='youtube.com')
	codeSourceOfTheProject= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='github.com')
	authorOfTheVideo = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	classCategory = forms.ChoiceField(widget=forms.Select, choices=CLASS_CATEGORY, required=False, initial='classCategory')
	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)


	class Meta:
		model = Post
		fields = ('content', 'lessonLink', 'codeSourceOfTheProject', 'caption', 'authorOfTheVideo', 'classCategory', 'tags')


 
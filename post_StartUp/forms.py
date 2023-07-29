from django import forms
from post_StartUp.models import Post_StartUp

from django.forms import ClearableFileInput
 
class NewPostForm_StartUp(forms.ModelForm):
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

	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	lessonLink= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='youtube.com')
	codeSourceOfTheProject= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='founderinstitute.com')
	authorOfTheVideo = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	classCategory = forms.ChoiceField(widget=forms.Select, choices=CLASS_CATEGORY, required=False, initial='classCategory')
	tagsStartUp = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True) 


	class Meta:
		model = Post_StartUp
		fields = ('content', 'lessonLink', 'codeSourceOfTheProject', 'caption', 'authorOfTheVideo', 'classCategory', 'tagsStartUp')

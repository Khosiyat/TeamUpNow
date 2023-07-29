from django import forms

from stories.models import Story

from django.forms import ClearableFileInput

class NewStoryForm(forms.ModelForm):
	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

	class Meta:
		model = Story
		fields = ('content', 'caption')
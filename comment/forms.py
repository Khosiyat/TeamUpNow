from django import forms
from comment.models import Comment, Comment_StartUp

class CommentForm(forms.ModelForm):
	COMMENT_CATEGORY = [
	('bug', 'bug'), 
	('solution', 'solution'),
	('question', 'question'),
	('feedback', 'feedback'),
]
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), required=False)
	comment_category = forms.ChoiceField(widget=forms.Select, choices=COMMENT_CATEGORY, required=True, initial='comment_category')
	bug_code= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='bug_code')

	class Meta:
		model = Comment
		fields = ('body','comment_category', 'bug_code')

class CommentForm_StartUp(forms.ModelForm):
	COMMENT_CATEGORY = [
	('solution', 'solution'),
	('question', 'question'),
	('feedback', 'feedback'),
]
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), required=False)
	comment_category = forms.ChoiceField(widget=forms.Select, choices=COMMENT_CATEGORY, required=True, initial='comment_category')
	bug_code= forms.URLField(widget=forms.TextInput(), max_length=50, required=False, initial='bug_code')

	class Meta:
		model = Comment_StartUp
		fields = ('body','comment_category', 'bug_code')

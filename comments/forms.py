from django import forms

class CommentForm(forms.Form):
    book = forms.CharField(widget=forms.HiddenInput())
    chapter = forms.CharField(widget=forms.HiddenInput())
    example = forms.CharField(widget=forms.HiddenInput())
    page = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    email = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('title', None) is None:
            raise forms.ValidationError('Title cannot be empty.')
        if cleaned_data.get('body', None) is None:
            raise forms.ValidationError('Description cannot be empty.')
        return cleaned_data

class ReplyForm(forms.Form):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    body = forms.CharField(widget=forms.Textarea)
    email = forms.CharField()

    def clean(self):
        return self.cleaned_data

# myapp/forms.py
from django import forms
from .models import UserText

class UserTextForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='Enter Text')

    class Meta:
        model = UserText
        fields = ['first_name', 'last_name', 'text']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.encrypted_text = self.cleaned_data['text']
        if commit:
            instance.save()
        return instance

class DecryptTextForm(forms.Form):
    user_id = forms.IntegerField(label='User ID')


class UserTextSearchForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

class UserTextUpdateForm(forms.ModelForm):
    class Meta:
        model = UserText
        fields = ['encrypted_text']
        widgets = {
            'encrypted_text': forms.Textarea(attrs={'rows': 5}),
        }



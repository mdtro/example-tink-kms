from django import forms


class GitHubTokenForm(forms.Form):
    token = forms.CharField(widget=forms.PasswordInput)

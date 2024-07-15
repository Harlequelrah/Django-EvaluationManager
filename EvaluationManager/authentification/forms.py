from django import forms


class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,label='Nom d\'utilisateur')
    password=forms.CharField(max_length=100,label='Mot de passe',widget=forms.PasswordInput)

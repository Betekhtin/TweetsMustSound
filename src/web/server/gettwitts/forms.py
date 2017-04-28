from django import forms


class LoginField(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100) #TODO: change 'your name'

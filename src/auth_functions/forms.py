from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    username = forms.CharField(max_length=150)
    email    = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm  = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('confirm'):
            raise forms.ValidationError("password and confirm password do not match")
        return data
    

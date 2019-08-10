from django import forms 

class AccountForm(forms.Form):
    nom = forms.CharField(max_length=100,
    widget = forms.TextInput(attrs={'class':'form-control'}),
    reqiuired = True
    placeholder= "Nom"
    )
    prenom = forms.CharField(max_length=100,
    widget = forms.TextInput(attrs={'class':'form-control'}),
    reqiuired = True
    )
    mail = forms.EmailField(max_length=100,
    widget = forms.TextInput(attrs={'class':'form-control'}),
    reqiuired = True
    )
    password = forms.PasswordField(max_length=100,
    widget = forms.TextInput(attrs={'class':'form-control'}),
    reqiuired = True
    )
    cpassword = forms.PasswordField(max_length=100,
    widget = forms.TextInput(attrs={'class':'form-control'}),
    reqiuired = True
    )
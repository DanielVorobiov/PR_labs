from django import forms


class SendMail(forms.Form):
    widgets = {
        "email": forms.EmailInput(attrs={
            "type": "email",
            "id": "email",
            "name": "email",
            "placeholder": "example@gmail.com",
        }),
        "subject": forms.TextInput(attrs={
            'type': "text",
            'id': "title",
            'name': "title",
            'placeholder': "The subject is..",
        }),
        "body": forms.Textarea(attrs={
            "rows": "4",
            "cols": "50",
            "name": "msg",
            "id": "msg",
            "placeholder": "Your message goes here"
        }),
        "file": forms.FileInput(attrs={
            "type": "docfile",
            "id": "id_docfile",
            "name": "docfile"
        })

    }
    email = forms.EmailField(
        label="Email", max_length=50, widget=widgets["email"])
    subject = forms.CharField(
        label="subject", max_length=50, widget=widgets["subject"])
    body = forms.CharField(widget=widgets["body"])
    docfile = forms.FileField(required=False)


class Login(forms.Form):

    widgets = {
        "mail": forms.EmailInput(attrs={
            "type": "email",
            "id": "email",
            "name": "email"
        }),
        "password": forms.TextInput(attrs={
            "type": "password",
            "id": "pwd",
            "name": "pwd"
        })
    }
    mail = forms.EmailField(label="Mail", widget=widgets["mail"])
    password = forms.CharField(widget=widgets["password"])

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email Address")
    subject = forms.CharField(max_length=200, required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
from django import forms

class LogFileUploadForm(forms.Form):
    log_file = forms.FileField(label="Upload Log File", widget=forms.FileInput(attrs={
        'accept': '.log'
    }))
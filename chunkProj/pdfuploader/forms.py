from django import forms
from .models import PDFUpload

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['title', 'file']
        
class MultiPDFUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

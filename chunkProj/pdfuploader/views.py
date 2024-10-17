from django.shortcuts import render, redirect
from .forms import MultiPDFUploadForm
from .models import PDFUpload

def upload_pdfs(request):
    if request.method == 'POST':
        form = MultiPDFUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if form.is_valid():
            for file in files:
                PDFUpload.objects.create(title=file.name, file=file)
            return redirect('success')
    else:
        form = MultiPDFUploadForm()

    return render(request, 'pdfuploader/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'pdfuploader/success.html')

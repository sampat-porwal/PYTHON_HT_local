from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import PdfFileForm
from .models import PdfFile
from django.http import JsonResponse
import json


def ajax_view_post_method(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            ids = data.get('ids')
            pdf_files = PdfFile.objects.filter(id__in=ids)
            pdf_data = [                
                        {                           
                            'in_processing': pdf_file.in_processing, 
                            'ID': pdf_file.id,                
                        }
                        for pdf_file in pdf_files
                       if not pdf_file.in_processing
                  ]       

            # Process the data as needed
            response_data = {
                'message': message,  # Echo the message back
                'processing_done': pdf_data
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def ajax_view_get_method(request):    
    try:
        # pdf_files = PdfFile.objects.all()[0] 
        pdf_files = PdfFile.objects.filter(in_processing=True)        
        pdf_data = [
                        {
                            'file_name': pdf_file.file_name,  # Access individual object attributes
                            'in_processing': pdf_file.in_processing, 
                            'ID': pdf_file.id,                
                        }
                        for pdf_file in pdf_files
                  ]  
        # Your logic here, for example:
        data = {
            'message': 'Hello from Django!',
            'pdf_files': pdf_data,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  
class PdfFileListView(LoginRequiredMixin, ListView):
    model = PdfFile
    template_name = "pdf_list.html"
    context_object_name = "pdf_files"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(file_name__icontains=search_query)
        return queryset.filter(user=self.request.user).order_by('-created_at')


class PdfFileUploadView(LoginRequiredMixin, CreateView):
    model = PdfFile
    form_class = PdfFileForm
    template_name = "pdf_list.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect("pdf-list")

    def get_success_url(self):
        return reverse_lazy("pdf-list")


class PdfFileDeleteView(LoginRequiredMixin, DeleteView):
    model = PdfFile
    success_url = reverse_lazy("pdf-list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            messages.success(request, "PDF file deleted successfully.", extra_tags="pdf_delete")
        else:
            messages.error(
                request,
                "You do not have permission to delete this file.",
                extra_tags="pdf_delete",
            )
        return super().post(request, *args, **kwargs)


def chat_view(request):
    selected_pdf_ids = request.GET.get('pdf_ids')
    if selected_pdf_ids:
        pdf_id_list = []
        for id in selected_pdf_ids.split(','):
            try:
                pdf_id_list.append(int(id))
            except ValueError:
                messages.error(request, "PDF ids are invalid.")
                return redirect('pdf-list')

        pdf_files = PdfFile.objects.filter(id__in=pdf_id_list, user=request.user)
        if pdf_files.count() == len(pdf_id_list):
            return render(request, "chat.html", {'selected_ids': pdf_id_list})
        else:
            messages.error(request, "PDF ids are invalid.")
            return redirect('pdf-list')
    else:
        messages.error(request, "Select PDF to start chat.")
        return redirect('pdf-list')

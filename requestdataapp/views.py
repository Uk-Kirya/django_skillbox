from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .forms import UserBioForm, FileUploadForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def file_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()
            my_file = form.cleaned_data["my_file"]
            filename = fs.save(my_file.name, my_file)
    else:
        form = FileUploadForm()

    context = {
        "form": form,
    }

    return render(request, "requestdataapp/file-form.html", context=context)

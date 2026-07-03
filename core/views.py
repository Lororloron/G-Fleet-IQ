from django.shortcuts import render

# Create your views here.
def loads(request):
    loads = Load.objects.all()

    return render(
        request,
        "dashboard/loads.html",
        {"loads": loads},
    )
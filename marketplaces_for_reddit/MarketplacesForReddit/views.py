from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'test': "Hello, world. You're at the Marketplaces For Reddit index."
    }
    return render(request, 'home/index.html', context)

from django.shortcuts import render
from .models import Client

# Create your views here.
def main(request):
    return render(request, 'base.html')


def users(request):
    context = {
        'users': Client.objects.all(),
    }
    return render(request, 'users.html', context)

def write(request):
    return render(request, 'write.html')
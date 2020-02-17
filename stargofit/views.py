from django.shortcuts import render
from django.http import HttpResponseRedirect


def start_page(request):
    template_name = 'start_page.html'
    context = {}
    return render(request, template_name, context)

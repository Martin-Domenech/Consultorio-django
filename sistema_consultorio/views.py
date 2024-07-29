from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def inicio(request):
    contexto={}
    Http_response = render(
        request=request,
        template_name='inicio.html',
        context=contexto,
    )
    return Http_response

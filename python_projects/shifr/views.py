from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserTextForm, UserTextSearchForm, UserTextUpdateForm
from cryptography.fernet import Fernet
from django.conf import settings
from .models import UserText
from django.core.serializers import serialize
import json

# Create your views here.


def home(request):
    return render(request, 'index.html')

def shifrlash(request):
    shifrlar = UserText.objects.all().order_by('-id')
    if request.method == 'POST':
        form = UserTextForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shifrlash')
    else:
        form = UserTextForm()
    return render(request, 'shifrlash.html', {'form': form, 'shifrlar': shifrlar})


def deshifrlash(request):
    shifrlar = UserText.objects.all()
    shifrlar_json = json.dumps(list(shifrlar.values('first_name', 'last_name')))
    decrypted_texts = []
    first_name = None
    last_name = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_text_list = UserText.objects.filter(first_name=first_name, last_name=last_name)
        if user_text_list.exists():
            for user_text in user_text_list:
                decrypted_texts.append(user_text.get_decrypted_text())
    return render(request, 'deshifrlash.html', {
        'shifrlar': shifrlar,
        'shifrlar_json': shifrlar_json,
        'decrypted_texts': decrypted_texts,
        'first_name': first_name,
        'last_name': last_name
    })


def edit(request):
    search_form = UserTextSearchForm()
    user_texts = UserText.objects.all()
    shifrlar_json = json.dumps(list(user_texts.values('first_name', 'last_name')))
    search_results = None
    update_form = None
    user_text = None

    if request.method == 'POST':
        if 'search' in request.POST:
            search_form = UserTextSearchForm(request.POST)
            if search_form.is_valid():
                first_name = search_form.cleaned_data['first_name']
                last_name = search_form.cleaned_data['last_name']
                if last_name:
                    search_results = UserText.objects.filter(first_name=first_name, last_name=last_name)
                else:
                    search_results = UserText.objects.filter(first_name=first_name)
        
        if 'select' in request.POST:
            user_text_id = request.POST.get('user_text_id')
            user_text = get_object_or_404(UserText, id=user_text_id)
            update_form = UserTextUpdateForm(initial={'encrypted_text': user_text.get_decrypted_text()})

        if 'update' in request.POST:
            user_text = get_object_or_404(UserText, id=request.POST.get('user_text_id'))
            update_form = UserTextUpdateForm(request.POST)
            if update_form.is_valid():
                encrypted_text = update_form.cleaned_data['encrypted_text']
                user_text.encrypted_text = encrypted_text
                user_text._updating = True  # Set the flag to indicate an update operation
                user_text.save()
                return redirect('edit')

    return render(request, 'edit.html', {
        'search_form': search_form,
        'update_form': update_form,
        'shifrlar_json': shifrlar_json,
        'user_text': user_text,
        'user_texts': user_texts,
        'search_results': search_results,
    })

    
def delete(request):
    search_form = UserTextSearchForm()
    delete_form = None
    user_text = None
    user_texts = UserText.objects.all()
    shifrlar_json = json.dumps(list(user_texts.values('first_name', 'last_name')))
    search_results = None

    if request.method == 'POST':
        if 'search' in request.POST:
            search_form = UserTextSearchForm(request.POST)
            if search_form.is_valid():
                first_name = search_form.cleaned_data['first_name']
                last_name = search_form.cleaned_data['last_name']
                search_results = UserText.objects.filter(first_name=first_name, last_name=last_name)
                if search_results.exists():
                    delete_form = UserTextUpdateForm(instance=search_results.first())

        if 'delete' in request.POST:
            user_text = get_object_or_404(UserText, id=request.POST.get('user_text_id'))
            user_text.delete()
            return redirect('shifrlash')

    return render(request, 'delete.html', {
        'search_form': search_form,
        'delete_form': delete_form,
        'user_text': user_text,
        'user_texts': user_texts,        
        'shifrlar_json': shifrlar_json,
        'search_results': search_results,
    })


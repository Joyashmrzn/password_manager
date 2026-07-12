from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VaultEntry


@login_required
def vault_list(request):
    entries = VaultEntry.objects.filter(user=request.user)
    return render(request, 'vault_list.html', {'entries': entries})


@login_required
def vault_add(request):
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        site_url = request.POST.get('site_url')
        site_username = request.POST.get('site_username')
        password = request.POST.get('password')

        entry = VaultEntry(
            user=request.user,
            site_name=site_name,
            site_url=site_url,
            site_username=site_username,
        )
        entry.set_password(password)
        entry.save()
        messages.success(request, 'Entry saved.')
        return redirect('vault_list')
    return render(request, 'vault_add.html')


@login_required
def vault_view_password(request, pk):
    entry = get_object_or_404(VaultEntry, pk=pk, user=request.user)
    decrypted = entry.get_password()
    return render(request, 'vault_detail.html', {'entry': entry, 'password': decrypted})


@login_required
def vault_delete(request, pk):
    entry = get_object_or_404(VaultEntry, pk=pk, user=request.user)
    entry.delete()
    messages.success(request, 'Entry deleted.')
    return redirect('vault_list')
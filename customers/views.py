from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def customer_list(request):
    return render(request, 'customers/customer_list.html', {'message': 'Módulo de clientes em desenvolvimento'})

@login_required
def customer_create(request):
    return render(request, 'customers/customer_form.html', {'message': 'Criar cliente em desenvolvimento'})

@login_required
def customer_detail(request, pk):
    return render(request, 'customers/customer_detail.html', {'message': f'Detalhes do cliente {pk} em desenvolvimento'})

@login_required
def customer_edit(request, pk):
    return render(request, 'customers/customer_form.html', {'message': f'Editar cliente {pk} em desenvolvimento'})

@login_required
def customer_delete(request, pk):
    return render(request, 'customers/customer_confirm_delete.html', {'message': f'Excluir cliente {pk} em desenvolvimento'})

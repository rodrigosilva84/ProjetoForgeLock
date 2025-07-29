from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    return render(request, 'products/product_list.html', {'message': 'Módulo de produtos em desenvolvimento'})

@login_required
def product_create(request):
    return render(request, 'products/product_form.html', {'message': 'Criar produto em desenvolvimento'})

@login_required
def product_detail(request, pk):
    return render(request, 'products/product_detail.html', {'message': f'Detalhes do produto {pk} em desenvolvimento'})

@login_required
def product_edit(request, pk):
    return render(request, 'products/product_form.html', {'message': f'Editar produto {pk} em desenvolvimento'})

@login_required
def product_delete(request, pk):
    return render(request, 'products/product_confirm_delete.html', {'message': f'Excluir produto {pk} em desenvolvimento'})

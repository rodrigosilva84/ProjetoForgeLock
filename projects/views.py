from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def project_list(request):
    return render(request, 'projects/project_list.html', {'message': 'Módulo de projetos em desenvolvimento'})

@login_required
def project_create(request):
    return render(request, 'projects/project_form.html', {'message': 'Criar projeto em desenvolvimento'})

@login_required
def project_detail(request, pk):
    return render(request, 'projects/project_detail.html', {'message': f'Detalhes do projeto {pk} em desenvolvimento'})

@login_required
def project_edit(request, pk):
    return render(request, 'projects/project_form.html', {'message': f'Editar projeto {pk} em desenvolvimento'})

@login_required
def project_delete(request, pk):
    return render(request, 'projects/project_confirm_delete.html', {'message': f'Excluir projeto {pk} em desenvolvimento'})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
from core.models import Company


def get_user_company(request):
    """Retorna a empresa principal do usuário"""
    user = request.user
    company = user.get_primary_company()
    
    if not company:
        messages.error(request, _('Você precisa configurar uma empresa primeiro.'))
        return None
    
    return company


@login_required
def customer_list(request):
    """Lista de clientes da empresa do usuário"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    # Busca
    search = request.GET.get('search', '')
    customers = Customer.objects.filter(company=company)
    
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(document_number__icontains=search)
        )
    
    # Filtros
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        customers = customers.filter(is_active=True)
    elif status_filter == 'inactive':
        customers = customers.filter(is_active=False)
    
    # Ordenação
    order_by = request.GET.get('order_by', 'name')
    if order_by in ['name', 'email', 'created_at']:
        customers = customers.order_by(order_by)
    else:
        customers = customers.order_by('name')
    
    context = {
        'customers': customers,
        'search': search,
        'status_filter': status_filter,
        'order_by': order_by,
        'total_customers': customers.count(),
        'active_customers': customers.filter(is_active=True).count(),
    }
    
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_create(request):
    """Criar novo cliente"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, user=request.user)
        if form.is_valid():
            # Verificar se já existe cliente com este e-mail na empresa
            email = form.cleaned_data.get('email')
            if email and Customer.objects.filter(company=company, email=email).exists():
                form.add_error('email', _('Já existe um cliente com este e-mail'))
            else:
                customer = form.save(commit=False)
                customer.company = company
                customer.save()
                
                messages.success(request, _('Cliente criado com sucesso!'))
                return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(user=request.user)
    
    context = {
        'form': form,
        'title': _('Novo Cliente'),
        'submit_text': _('Criar Cliente'),
    }
    
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_detail(request, pk):
    """Detalhes do cliente"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    customer = get_object_or_404(Customer, pk=pk, company=company)
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'customers/customer_detail.html', context)


@login_required
def customer_edit(request, pk):
    """Editar cliente"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    customer = get_object_or_404(Customer, pk=pk, company=company)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Cliente atualizado com sucesso!'))
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer, user=request.user)
    
    context = {
        'form': form,
        'customer': customer,
        'title': _('Editar Cliente'),
        'submit_text': _('Salvar Alterações'),
    }
    
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_delete(request, pk):
    """Excluir cliente"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    customer = get_object_or_404(Customer, pk=pk, company=company)
    
    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, _('Cliente "{}" excluído com sucesso!').format(customer_name))
        return redirect('customers:customer_list')
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'customers/customer_confirm_delete.html', context)


@login_required
def customer_toggle_status(request, pk):
    """Ativar/desativar cliente"""
    company = get_user_company(request)
    if not company:
        return JsonResponse({'success': False, 'message': _('Empresa não configurada')})
    
    customer = get_object_or_404(Customer, pk=pk, company=company)
    
    if request.method == 'POST':
        customer.is_active = not customer.is_active
        customer.save()
        
        status_text = _('ativado') if customer.is_active else _('desativado')
        return JsonResponse({
            'success': True,
            'message': _('Cliente {} com sucesso!').format(status_text),
            'is_active': customer.is_active
        })
    
    return JsonResponse({'success': False, 'message': _('Método não permitido')})


@login_required
def customer_search(request):
    """Busca AJAX de clientes"""
    company = get_user_company(request)
    if not company:
        return JsonResponse({'results': []})
    
    search = request.GET.get('q', '')
    if len(search) < 2:
        return JsonResponse({'results': []})
    
    customers = Customer.objects.filter(
        company=company,
        is_active=True
    ).filter(
        Q(name__icontains=search) |
        Q(email__icontains=search) |
        Q(phone__icontains=search)
    )[:10]
    
    results = []
    for customer in customers:
        results.append({
            'id': customer.pk,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
        })
    
    return JsonResponse({'results': results})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.utils import translation

from .models import Product, ProductImage, Category, ProductType, Currency, Scale
from .forms import ProductForm, CategoryForm, ProductTypeForm, ScaleForm
from .translations import get_product_type_translation, get_category_translation
from core.models import Company, Country


def get_user_company(request):
    """Retorna a empresa principal do usuário"""
    user = request.user
    company = user.get_primary_company()
    
    if not company:
        messages.error(request, _('Você precisa configurar uma empresa primeiro.'))
        return None
    
    return company


@login_required
def product_list(request):
    """Lista de produtos com filtros"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    products = Product.objects.filter(company=company)  # Filtrar por empresa
    
    # Filtros
    search = request.GET.get('search', '')
    product_type = request.GET.get('product_type', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    status = request.GET.get('status', '')  # Novo filtro de status
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(scale__icontains=search)
        )
    
    if product_type:
        products = products.filter(product_type_id=product_type)
    
    if category:
        products = products.filter(category_id=category)
    
    if min_price:
        products = products.filter(sale_price__gte=min_price)
    
    if max_price:
        products = products.filter(sale_price__lte=max_price)
    
    # Filtro de status
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    # Se status estiver vazio, mostra todos (ativo e inativo)
    
    # Paginação
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros com traduções
    current_language = translation.get_language()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    
    # Aplicar traduções aos dados
    for product_type in product_types:
        product_type.translated_name = get_product_type_translation(
            product_type.name, current_language
        )
    
    for category in categories:
        category.translated_name = get_category_translation(
            category.name, current_language
        )
    
    context = {
        'page_obj': page_obj,
        'product_types': product_types,
        'categories': categories,
        'search': search,
        'product_type': product_type,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'status': status,  # Adicionando status ao contexto
    }
    
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Detalhes do produto"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    product = get_object_or_404(Product, pk=pk, company=company)  # Filtrar por empresa
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)


@login_required
def product_create(request):
    """Criar novo produto"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.company = company  # Associar à empresa
            product.save()
            
            # Processa as imagens
            images = request.FILES.getlist('images')
            if len(images) > 5:
                messages.error(request, _('Máximo 5 imagens permitidas'))
                product.delete()
                return render(request, 'products/product_form.html', {'form': form})
            
            for i, image in enumerate(images):
                if image.size > 10 * 1024 * 1024:  # 10MB
                    messages.error(request, _('Cada imagem deve ter no máximo 10MB'))
                    product.delete()
                    return render(request, 'products/product_form.html', {'form': form})
                
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=(i == 0),  # Primeira imagem é principal
                    order_index=i
                )
            
            messages.success(request, _('Produto criado com sucesso!'))
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    # Dados com traduções
    current_language = translation.get_language()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    
    # Aplicar traduções
    for product_type in product_types:
        product_type.translated_name = get_product_type_translation(
            product_type.name, current_language
        )
    
    for category in categories:
        category.translated_name = get_category_translation(
            category.name, current_language
        )
    
    context = {
        'form': form,
        'product_types': product_types,
        'categories': categories,
        'currencies': Currency.objects.all(),
    }

    return render(request, 'products/product_form.html', context)


@login_required
def product_edit(request, pk):
    """Editar produto"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    product = get_object_or_404(Product, pk=pk, company=company)  # Filtrar por empresa

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            
            # Processa novas imagens
            images = request.FILES.getlist('images')
            if images:
                # Remove imagens antigas se novas foram enviadas
                product.images.all().delete()
                
                for i, image in enumerate(images):
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_primary=(i == 0),
                        order_index=i
                    )
            
            messages.success(request, _('Produto atualizado com sucesso!'))
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    # Dados com traduções
    current_language = translation.get_language()
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    
    # Aplicar traduções
    for product_type in product_types:
        product_type.translated_name = get_product_type_translation(
            product_type.name, current_language
        )
    
    for category in categories:
        category.translated_name = get_category_translation(
            category.name, current_language
        )
    
    context = {
        'form': form,
        'product': product,
        'product_types': product_types,
        'categories': categories,
        'currencies': Currency.objects.all(),
    }

    return render(request, 'products/product_form.html', context)


@login_required
def product_delete(request, pk):
    """Excluir produto"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    product = get_object_or_404(Product, pk=pk, company=company)  # Filtrar por empresa
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, _('Produto excluído com sucesso!'))
        return redirect('products:product_list')
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_confirm_delete.html', context)


@login_required
def product_toggle_status(request, pk):
    """Alternar status ativo/inativo do produto"""
    company = get_user_company(request)
    if not company:
        return redirect('company_setup')
    
    product = get_object_or_404(Product, pk=pk, company=company)  # Filtrar por empresa
    product.is_active = not product.is_active
    product.save()
    
    status = _('ativado') if product.is_active else _('desativado')
    messages.success(request, _(f'Produto {status} com sucesso!'))
    
    return redirect('products:product_list')


# Views para categorias (módulo separado)
@login_required
def category_list(request):
    """Lista de categorias com filtros de pesquisa"""
    categories = Category.objects.all().order_by('name')
    
    # Filtros de pesquisa
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        categories = categories.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if status == 'active':
        categories = categories.filter(is_active=True)
    elif status == 'inactive':
        categories = categories.filter(is_active=False)
    # Se status estiver vazio, mostra todos (ativo e inativo)
    
    context = {
        'categories': categories,
        'search': search,
        'status': status,
    }
    
    return render(request, 'products/category_list.html', context)


@login_required
def category_create(request):
    """Criar nova categoria"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Categoria criada com sucesso!'))
            return redirect('products:category_list')
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'products/category_form.html', context)


@login_required
def category_edit(request, pk):
    """Editar categoria"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Categoria atualizada com sucesso!'))
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }

    return render(request, 'products/category_form.html', context)


@login_required
def category_delete(request, pk):
    """Excluir categoria"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        # Verificar se há produtos usando esta categoria
        if Product.objects.filter(category=category).exists():
            messages.error(request, _('Não é possível excluir uma categoria que possui produtos!'))
        else:
            category.delete()
            messages.success(request, _('Categoria excluída com sucesso!'))
        
        return redirect('products:category_list')
    
    context = {
        'category': category,
    }
    
    return render(request, 'products/category_confirm_delete.html', context)


@login_required
def category_toggle_status(request, pk):
    """Ativar/desativar categoria"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.is_active = not category.is_active
        category.save()
        
        status_text = _('ativada') if category.is_active else _('desativada')
        messages.success(request, _('Categoria {} com sucesso!').format(status_text))
        return redirect('products:category_list')
    
    return render(request, 'products/category_confirm_toggle.html', {'category': category})


@login_required
def scale_list(request):
    """Lista de escalas com filtros de pesquisa"""
    scales = Scale.objects.all().order_by('name')
    
    # Filtros de pesquisa
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        scales = scales.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if status == 'active':
        scales = scales.filter(is_active=True)
    elif status == 'inactive':
        scales = scales.filter(is_active=False)
    # Se status estiver vazio, mostra todos (ativo e inativo)
    
    context = {
        'scales': scales,
        'search': search,
        'status': status,
    }
    
    return render(request, 'products/scale_list.html', context)

@login_required
def scale_create(request):
    """Criar nova escala"""
    if request.method == 'POST':
        form = ScaleForm(request.POST)
        if form.is_valid():
            scale = form.save()
            messages.success(request, _('Escala criada com sucesso!'))
            return redirect('products:scale_list')
    else:
        form = ScaleForm()
    
    return render(request, 'products/scale_form.html', {'form': form})

@login_required
def scale_edit(request, pk):
    """Editar escala"""
    scale = get_object_or_404(Scale, pk=pk)
    if request.method == 'POST':
        form = ScaleForm(request.POST, instance=scale)
        if form.is_valid():
            form.save()
            messages.success(request, _('Escala atualizada com sucesso!'))
            return redirect('products:scale_list')
    else:
        form = ScaleForm(instance=scale)
    
    return render(request, 'products/scale_form.html', {'form': form, 'scale': scale})

@login_required
def scale_delete(request, pk):
    """Excluir escala"""
    scale = get_object_or_404(Scale, pk=pk)
    if request.method == 'POST':
        scale.delete()
        messages.success(request, _('Escala excluída com sucesso!'))
        return redirect('products:scale_list')
    
    return render(request, 'products/scale_confirm_delete.html', {'scale': scale})

@login_required
def scale_toggle_status(request, pk):
    """Ativar/desativar escala"""
    scale = get_object_or_404(Scale, pk=pk)
    
    if request.method == 'POST':
        scale.is_active = not scale.is_active
        scale.save()
        
        status_text = _('ativada') if scale.is_active else _('desativada')
        messages.success(request, _('Escala {} com sucesso!').format(status_text))
        return redirect('products:scale_list')
    
    return render(request, 'products/scale_confirm_toggle.html', {'scale': scale})


@login_required
def product_type_create_ajax(request):
    """Criar tipo de produto via AJAX"""
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            product_type = form.save()
            return JsonResponse({
                'success': True,
                'id': product_type.id,
                'name': product_type.name,
                'message': _('Tipo de produto criado com sucesso!')
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    form = ProductTypeForm()
    return render(request, 'products/product_type_form_ajax.html', {'form': form})

@login_required
def category_create_ajax(request):
    """Criar categoria via AJAX"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                'success': True,
                'id': category.id,
                'name': category.name,
                'message': _('Categoria criada com sucesso!')
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    form = CategoryForm()
    return render(request, 'products/category_form_ajax.html', {'form': form})


@login_required
def scale_create_ajax(request):
    """Criar escala via AJAX"""
    if request.method == 'POST':
        form = ScaleForm(request.POST)
        if form.is_valid():
            scale = form.save()
            return JsonResponse({
                'success': True,
                'id': scale.id,
                'name': scale.name,
                'message': _('Escala criada com sucesso!')
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    form = ScaleForm()
    return render(request, 'products/scale_form_ajax.html', {'form': form})


# Views para ProductType (módulo separado)
@login_required
def product_type_list(request):
    """Lista de tipos de produto com filtros de pesquisa"""
    product_types = ProductType.objects.all().order_by('name')
    
    # Filtros de pesquisa
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        product_types = product_types.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if status == 'active':
        product_types = product_types.filter(is_active=True)
    elif status == 'inactive':
        product_types = product_types.filter(is_active=False)
    # Se status estiver vazio, mostra todos (ativo e inativo)
    
    context = {
        'product_types': product_types,
        'search': search,
        'status': status,
    }
    
    return render(request, 'products/product_type_list.html', context)


@login_required
def product_type_create(request):
    """Criar novo tipo de produto"""
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tipo de produto criado com sucesso!'))
            return redirect('products:product_type_list')
    else:
        form = ProductTypeForm()
    
    return render(request, 'products/product_type_form.html', {'form': form})


@login_required
def product_type_edit(request, pk):
    """Editar tipo de produto"""
    product_type = get_object_or_404(ProductType, pk=pk)
    
    if request.method == 'POST':
        form = ProductTypeForm(request.POST, instance=product_type)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tipo de produto atualizado com sucesso!'))
            return redirect('products:product_type_list')
    else:
        form = ProductTypeForm(instance=product_type)
    
    return render(request, 'products/product_type_form.html', {'form': form, 'product_type': product_type})


@login_required
def product_type_toggle_status(request, pk):
    """Ativar/desativar tipo de produto"""
    product_type = get_object_or_404(ProductType, pk=pk)
    
    if request.method == 'POST':
        product_type.is_active = not product_type.is_active
        product_type.save()
        
        status_text = _('ativado') if product_type.is_active else _('desativado')
        messages.success(request, _('Tipo de produto {} com sucesso!').format(status_text))
        return redirect('products:product_type_list')
    
    return render(request, 'products/product_type_confirm_toggle.html', {'product_type': product_type})


# Views para Category (módulo separado)


@login_required
def category_toggle_status(request, pk):
    """Ativar/desativar categoria"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.is_active = not category.is_active
        category.save()
        
        status_text = _('ativada') if category.is_active else _('desativada')
        messages.success(request, _('Categoria {} com sucesso!').format(status_text))
        return redirect('products:category_list')
    
    return render(request, 'products/category_confirm_toggle.html', {'category': category})


# Views para Country (módulo separado)
@login_required
def country_list(request):
    """Lista de países com filtros de pesquisa"""
    countries = Country.objects.all().order_by('name')
    
    # Filtros de pesquisa
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        countries = countries.filter(
            Q(name__icontains=search) | 
            Q(code__icontains=search) |
            Q(ddi__icontains=search)
        )
    
    if status == 'active':
        countries = countries.filter(is_active=True)
    elif status == 'inactive':
        countries = countries.filter(is_active=False)
    # Se status estiver vazio, mostra todos (ativo e inativo)
    
    context = {
        'countries': countries,
        'search': search,
        'status': status,
    }
    
    return render(request, 'products/country_list.html', context)


@login_required
def country_edit(request, pk):
    """Editar país"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        # Processar dados do formulário
        name = request.POST.get('name')
        name_en = request.POST.get('name_en', '')
        name_es = request.POST.get('name_es', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if name:
            country.name = name
            country.name_en = name_en
            country.name_es = name_es
            country.is_active = is_active
            
            # Processar upload de bandeira
            if 'flag' in request.FILES:
                flag_file = request.FILES['flag']
                # Validar tipo de arquivo
                if flag_file.content_type.startswith('image/') or flag_file.name.endswith('.svg'):
                    try:
                        # Salvar o arquivo
                        import os
                        from django.conf import settings
                        
                        # Criar diretório se não existir
                        flag_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'flags')
                        os.makedirs(flag_dir, exist_ok=True)
                        
                        # Gerar nome do arquivo (apenas o código do país)
                        flag_filename = f"{country.code.lower()}.svg"
                        flag_path = os.path.join(flag_dir, flag_filename)
                        
                        # Salvar arquivo
                        with open(flag_path, 'wb+') as destination:
                            for chunk in flag_file.chunks():
                                destination.write(chunk)
                        
                        # Verificar se o arquivo foi salvo corretamente
                        if os.path.exists(flag_path) and os.path.getsize(flag_path) > 0:
                            # Atualizar campo flag no modelo (apenas o código do país)
                            country.flag = country.code.lower()
                            messages.success(request, _('Bandeira atualizada com sucesso!'))
                        else:
                            messages.error(request, _('Erro ao salvar a bandeira.'))
                    except Exception as e:
                        messages.error(request, _('Erro ao processar o upload da bandeira: {}').format(str(e)))
                else:
                    messages.error(request, _('Formato de arquivo não suportado. Use apenas imagens (PNG, JPG, SVG).'))
            
            country.save()
            messages.success(request, _('País atualizado com sucesso!'))
            return redirect('products:country_list')
        else:
            messages.error(request, _('Nome é obrigatório.'))
    
    # Preparar dados para o form
    form_data = {
        'name': country.name,
        'name_en': country.name_en,
        'name_es': country.name_es,
        'is_active': country.is_active
    }
    
    return render(request, 'products/country_form.html', {'country': country, 'form_data': form_data})


@login_required
def country_toggle_status(request, pk):
    """Ativar/desativar país"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        country.is_active = not country.is_active
        country.save()
        
        status_text = _('ativado') if country.is_active else _('desativado')
        messages.success(request, _('País {} com sucesso!').format(status_text))
        return redirect('products:country_list')
    
    return render(request, 'products/country_confirm_toggle.html', {'country': country})

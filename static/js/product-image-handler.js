/**
 * Handler para seleção de imagens de produto
 * Limita a 5 imagens e mostra preview
 */
class ProductImageHandler {
    constructor() {
        this.maxImages = 5;
        this.imageInput = document.getElementById('images');
        this.previewContainer = document.getElementById('image-preview');
        this.selectedFiles = [];
        
        if (this.imageInput) {
            this.init();
        }
    }
    
    init() {
        this.imageInput.addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files);
        });
        
        // Criar container de preview se não existir
        if (!this.previewContainer) {
            this.createPreviewContainer();
        }
    }
    
    createPreviewContainer() {
        // Usar o container que já existe no template
        this.previewContainer = document.getElementById('image-preview');
        if (this.previewContainer) {
            this.previewContainer.style.display = 'block';
        }
    }
    
    handleFileSelection(files) {
        const fileArray = Array.from(files);
        
        // Verificar se excede o limite
        if (this.selectedFiles.length + fileArray.length > this.maxImages) {
            alert(`Máximo ${this.maxImages} imagens permitidas. Você já selecionou ${this.selectedFiles.length} imagens.`);
            this.imageInput.value = '';
            return;
        }
        
        // Adicionar novos arquivos
        this.selectedFiles = [...this.selectedFiles, ...fileArray];
        
        // Atualizar preview
        this.updatePreview();
        
        // Atualizar input
        this.updateFileInput();
    }
    
    updatePreview() {
        const previewImages = document.getElementById('preview-images');
        if (!previewImages) return;
        
        previewImages.innerHTML = '';
        
        if (this.selectedFiles.length === 0) {
            this.previewContainer.style.display = 'none';
            return;
        }
        
        this.previewContainer.style.display = 'block';
        
        // Criar carrossel principal
        const carouselDiv = document.createElement('div');
        carouselDiv.className = 'col-12 mb-3';
        carouselDiv.innerHTML = `
            <div id="imageCarousel" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-inner">
                    ${this.selectedFiles.map((file, index) => `
                        <div class="carousel-item ${index === 0 ? 'active' : ''}">
                            <div class="d-flex justify-content-center align-items-center" style="height: 300px; background-color: #f8f9fa;">
                                <img src="" class="img-fluid" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Preview ${index + 1}">
                            </div>
                        </div>
                    `).join('')}
                </div>
                ${this.selectedFiles.length > 1 ? `
                    <button class="carousel-control-prev" type="button" data-bs-target="#imageCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Anterior</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#imageCarousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Próximo</span>
                    </button>
                ` : ''}
            </div>
        `;
        previewImages.appendChild(carouselDiv);
        
        // Criar miniaturas
        const thumbnailsDiv = document.createElement('div');
        thumbnailsDiv.className = 'col-12';
        thumbnailsDiv.innerHTML = `
            <div class="d-flex flex-wrap gap-2">
                ${this.selectedFiles.map((file, index) => `
                    <div class="position-relative" style="cursor: pointer;" onclick="productImageHandler.showImage(${index})">
                        <div class="d-flex justify-content-center align-items-center" style="height: 60px; width: 60px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 0.375rem;">
                            <img src="" class="img-fluid" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="Thumbnail ${index + 1}">
                        </div>
                        <button type="button" class="btn btn-sm btn-danger position-absolute" 
                                style="top: -5px; right: -5px;" onclick="event.stopPropagation(); productImageHandler.removeImage(${index})">
                            <i class="fas fa-times"></i>
                        </button>
                        <div class="text-center mt-1">
                            <small class="text-muted">${index === 0 ? 'Principal' : index + 1}</small>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        previewImages.appendChild(thumbnailsDiv);
        
        // Carregar imagens
        this.selectedFiles.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                // Atualizar carrossel
                const carouselImg = carouselDiv.querySelector(`.carousel-item:nth-child(${index + 1}) img`);
                if (carouselImg) carouselImg.src = e.target.result;
                
                // Atualizar miniatura
                const thumbnailImg = thumbnailsDiv.querySelector(`img[alt="Thumbnail ${index + 1}"]`);
                if (thumbnailImg) thumbnailImg.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    }
    
    showImage(index) {
        const carousel = document.getElementById('imageCarousel');
        if (carousel && typeof bootstrap !== 'undefined') {
            const bsCarousel = new bootstrap.Carousel(carousel);
            bsCarousel.to(index);
        } else if (carousel) {
            // Fallback se Bootstrap não estiver disponível
            const items = carousel.querySelectorAll('.carousel-item');
            items.forEach((item, i) => {
                item.classList.remove('active');
                if (i === index) {
                    item.classList.add('active');
                }
            });
        }
    }
    
    removeImage(index) {
        this.selectedFiles.splice(index, 1);
        this.updatePreview();
        this.updateFileInput();
    }
    
    updateFileInput() {
        // Criar um novo FileList com os arquivos selecionados
        const dt = new DataTransfer();
        this.selectedFiles.forEach(file => dt.items.add(file));
        this.imageInput.files = dt.files;
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.productImageHandler = new ProductImageHandler();
}); 
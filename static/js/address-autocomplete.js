/**
 * Address Autocomplete Service
 * Suporte a Brasil (ViaCEP) e outros países (OpenStreetMap)
 */

class AddressAutocomplete {
    constructor() {
        this.cache = {};
        this.rateLimiter = {
            lastRequest: 0,
            minInterval: 1000 // 1 segundo entre requisições
        };
    }

    /**
     * Busca endereço por CEP/Postal Code
     */
    async lookupAddress(postalCode, country = 'BR') {
        const cleanPostalCode = this.cleanPostalCode(postalCode);
        
        if (!cleanPostalCode) {
            return { error: 'CEP/Postal Code inválido' };
        }

        // Verificar cache primeiro
        const cacheKey = `${country}_${cleanPostalCode}`;
        if (this.cache[cacheKey]) {
            return this.cache[cacheKey];
        }

        // Respeitar rate limit
        if (!this.canMakeRequest()) {
            return { error: 'Aguarde um momento antes de tentar novamente' };
        }

        try {
            let result;
            
            if (country === 'BR') {
                result = await this.viaCepLookup(cleanPostalCode);
            } else {
                result = await this.openStreetMapLookup(cleanPostalCode, country);
            }

            // Cache do resultado
            this.cache[cacheKey] = result;
            this.rateLimiter.lastRequest = Date.now();

            return result;

        } catch (error) {
            console.error('Erro na busca de endereço:', error);
            return { error: 'Erro ao buscar endereço. Tente novamente.' };
        }
    }

    /**
     * Busca via ViaCEP (Brasil)
     */
    async viaCepLookup(cep) {
        const url = `https://viacep.com.br/ws/${cep}/json/`;
        
        const response = await fetch(url);
        const data = await response.json();

        if (data.erro) {
            return { error: 'CEP não encontrado' };
        }

        return {
            success: true,
            address: data.logradouro,
            neighborhood: data.bairro,
            city: data.localidade,
            state: data.uf,
            country: 'Brasil',
            postalCode: data.cep
        };
    }

    /**
     * Busca via OpenStreetMap (outros países)
     */
    async openStreetMapLookup(postalCode, country) {
        // Mapear códigos de país para nomes
        const countryMap = {
            'BR': 'Brasil',
            'US': 'United States',
            'GB': 'United Kingdom',
            'FR': 'France',
            'DE': 'Germany',
            'ES': 'Spain',
            'IT': 'Italy',
            'CA': 'Canada',
            'AU': 'Australia'
        };
        
        const countryName = countryMap[country] || country;
        
        // Buscar especificamente por código postal + país
        const searchQueries = [
            `https://nominatim.openstreetmap.org/search?postalcode=${postalCode}&country=${countryName}&format=json&limit=1&addressdetails=1`,
            `https://nominatim.openstreetmap.org/search?q=${postalCode},${countryName}&format=json&limit=1&addressdetails=1`,
            `https://nominatim.openstreetmap.org/search?postalcode=${postalCode}&format=json&limit=1&addressdetails=1`
        ];

        for (const url of searchQueries) {
            try {
                const response = await fetch(url);
                const data = await response.json();

                if (data && data.length > 0) {
                    const place = data[0];
                    
                    // Verificar se o resultado é do país correto
                    const resultCountry = place.address?.country || '';
                    if (country !== 'US' && resultCountry.toLowerCase() !== countryName.toLowerCase()) {
                        continue;
                    }
                    
                    return {
                        success: true,
                        address: this.extractStreetAddress(place),
                        city: this.extractCityFromPlace(place),
                        state: this.extractStateFromPlace(place),
                        country: resultCountry,
                        postalCode: postalCode
                    };
                }
            } catch (error) {
                console.error('Erro na busca:', error);
                continue;
            }
        }

        return { error: 'Postal Code não encontrado' };
    }

    /**
     * Extrai endereço da rua do resultado do OpenStreetMap
     */
    extractStreetAddress(place) {
        const address = place.address;
        if (!address) return '';
        
        // Tentar diferentes campos de endereço
        return address.road || address.street || address.highway || '';
    }

    /**
     * Extrai cidade do resultado do OpenStreetMap
     */
    extractCityFromPlace(place) {
        const address = place.address;
        if (!address) return '';
        
        // Tentar diferentes campos de cidade
        return address.city || address.town || address.village || address.municipality || '';
    }

    /**
     * Extrai estado do resultado do OpenStreetMap
     */
    extractStateFromPlace(place) {
        const address = place.address;
        if (!address) return '';
        
        // Tentar diferentes campos de estado
        return address.state || address.province || address.region || '';
    }

    /**
     * Limpa CEP/Postal Code
     */
    cleanPostalCode(postalCode) {
        return postalCode.replace(/\D/g, '');
    }

    /**
     * Verifica se pode fazer requisição (rate limit)
     */
    canMakeRequest() {
        return Date.now() - this.rateLimiter.lastRequest >= this.rateLimiter.minInterval;
    }

    /**
     * Aplica máscara de CEP brasileiro
     */
    applyCepMask(input) {
        let value = input.value.replace(/\D/g, '');
        value = value.replace(/(\d{5})(\d)/, '$1-$2');
        input.value = value;
    }

    /**
     * Aplica máscara de Postal Code internacional
     */
    applyPostalCodeMask(input, country) {
        let value = input.value;
        
        // Para códigos postais internacionais, permitir letras e números
        // Apenas remover caracteres especiais indesejados
        value = value.replace(/[^A-Za-z0-9\s\-]/g, '');
        
        input.value = value;
    }
}

// Instância global
window.addressAutocomplete = new AddressAutocomplete();

/**
 * Inicializa automação de endereço em um formulário
 */
function initAddressAutocomplete(options = {}) {
    const {
        postalCodeField = '#zip_code',
        addressField = '#address',
        cityField = '#city',
        stateField = '#state',
        countryField = '#country',
        numberField = '#number',
        loadingClass = 'loading',
        successClass = 'success',
        errorClass = 'error'
    } = options;

    const postalCodeInput = document.querySelector(postalCodeField);
    const addressInput = document.querySelector(addressField);
    const cityInput = document.querySelector(cityField);
    const stateInput = document.querySelector(stateField);
    const countryInput = document.querySelector(countryField);
    const numberInput = document.querySelector(numberField);

    if (!postalCodeInput) {
        console.error('Campo CEP não encontrado:', postalCodeField);
        return;
    }

    // Aplicar máscara de CEP/Postal Code
    postalCodeInput.addEventListener('input', function() {
        const country = countryInput ? countryInput.value : 'BR';
        const value = this.value;
        
        // Detectar se é código postal internacional (tem letras)
        const hasLetters = /[A-Za-z]/.test(value);
        
        if (hasLetters) {
            // Permitir letras para códigos internacionais
        } else if (country === 'BR') {
            addressAutocomplete.applyCepMask(this);
        } else {
            addressAutocomplete.applyPostalCodeMask(this, country);
        }
    });

    // Buscar endereço quando CEP perder foco
    postalCodeInput.addEventListener('blur', async function() {
        const postalCode = this.value;
        let country = countryInput ? countryInput.value : 'BR';

        if (!postalCode || postalCode.length < 3) {
            return;
        }

        // Detectar país baseado no valor do campo
        if (country && !isNaN(country)) {
            // Se é um número, é um ID de país, converter para BR
            country = 'BR';
        } else if (!country || country === '') {
            // Se não há país selecionado, tentar detectar automaticamente
            const cleanPostalCode = postalCode.replace(/\D/g, '');
            const hasLetters = /[A-Za-z]/.test(postalCode);
            
            if (hasLetters || cleanPostalCode.length !== 8) {
                country = 'US'; // Usar EUA como padrão para internacional
            } else {
                country = 'BR';
            }
        }

        // Adicionar classe de loading
        this.classList.add(loadingClass);
        this.classList.remove(successClass, errorClass);

        try {
            const result = await addressAutocomplete.lookupAddress(postalCode, country);

            if (result.success) {
                // Preencher campos automaticamente
                if (addressInput) {
                    addressInput.value = result.address || '';
                }
                if (cityInput) {
                    cityInput.value = result.city || '';
                }
                if (stateInput) {
                    stateInput.value = result.state || '';
                }
                // Não sobrescrever o país se já foi selecionado pelo usuário
                if (countryInput && !countryInput.value) {
                    countryInput.value = result.country || '';
                }

                // Adicionar classes de sucesso
                this.classList.remove(loadingClass);
                this.classList.add(successClass);

                // Focar no campo número
                if (numberInput) {
                    numberInput.focus();
                }

                // Mostrar mensagem de sucesso
                showMessage('Endereço encontrado! Complete com o número.', 'success');

            } else {
                // Adicionar classes de erro
                this.classList.remove(loadingClass);
                this.classList.add(errorClass);

                // Mostrar mensagem de erro
                showMessage(result.error || 'CEP não encontrado', 'error');
            }

        } catch (error) {
            console.error('Erro na busca de endereço:', error);
            // Adicionar classes de erro
            this.classList.remove(loadingClass);
            this.classList.add(errorClass);

            // Mostrar mensagem de erro
            showMessage('Erro ao buscar endereço. Tente novamente.', 'error');
        }
    });

    // Limpar classes quando usuário começar a digitar
    postalCodeInput.addEventListener('input', function() {
        this.classList.remove(successClass, errorClass);
    });
}

/**
 * Mostra mensagem de feedback
 */
function showMessage(message, type = 'info') {
    // Remover mensagens anteriores
    const existingMessage = document.querySelector('.address-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    // Criar nova mensagem
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} address-message mt-2`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
    `;

    // Inserir após o campo CEP
    const postalCodeField = document.querySelector('#zip_code');
    if (postalCodeField) {
        postalCodeField.parentNode.insertBefore(messageDiv, postalCodeField.nextSibling);
    }

    // Remover mensagem após 5 segundos
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
} 
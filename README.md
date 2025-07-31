# ForgeLock Web Platform

## Padrões de Internacionalização (i18n)

### **Regra Principal: SEMPRE usar `{% translate %}` nos templates**

**❌ NÃO fazer:**
```python
# forms.py
self.fields['field'].label = _("Label")
```

**✅ SEMPRE fazer:**
```html
<!-- template.html -->
<label>{% translate "Label" %}</label>
```

### **Por que esse padrão?**
1. **Consistência:** Todas as traduções ficam nos templates
2. **Facilidade:** Não precisa gerenciar traduções no código Python
3. **Manutenibilidade:** Mudanças de texto ficam centralizadas
4. **Evita duplicatas:** Não há conflito entre form labels e template labels

### **Estrutura de Traduções:**
- **Templates:** `{% translate "Texto" %}`
- **Python:** `_("Texto")` apenas para mensagens dinâmicas
- **Arquivos .po:** Manter organizados sem duplicatas

### **Checklist para novos formulários:**
- [ ] Labels no template com `{% translate %}`
- [ ] Não definir labels no `__init__` do form
- [ ] Adicionar traduções nos arquivos .po
- [ ] Testar em todos os idiomas 
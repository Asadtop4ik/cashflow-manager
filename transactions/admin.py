from django.contrib import admin
from django import forms
from django.templatetags.static import static
from .models import Status, Type, Category, Subcategory, Transaction

class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize category and subcategory dropdowns
        if 'type' in self.fields:
            self.fields['category'].queryset = Category.objects.none()
            if self.instance and self.instance.type_id:
                self.fields['category'].queryset = Category.objects.filter(type_id=self.instance.type_id)
            elif 'type' in self.data:
                try:
                    type_id = int(self.data.get('type'))
                    self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
                except (ValueError, TypeError):
                    pass
        if 'category' in self.fields:
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            if self.instance and self.instance.category_id:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=self.instance.category_id)
            elif 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
                except (ValueError, TypeError):
                    pass

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')

        # Validate required fields
        if not type:
            raise forms.ValidationError("Type is required.")
        if not category:
            raise forms.ValidationError("Category is required.")
        if not subcategory:
            raise forms.ValidationError("Subcategory is required.")
        if amount is None:
            raise forms.ValidationError("Amount is required.")
        if date is None:
            raise forms.ValidationError("Date is required.")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

        # Validate logical dependencies
        if category and type and category.type != type:
            raise forms.ValidationError("Selected category does not belong to the selected type.")
        if subcategory and category and subcategory.category != category:
            raise forms.ValidationError("Selected subcategory does not belong to the selected category.")

        return cleaned_data

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
    list_filter = ['date', 'status', 'type', 'category', 'subcategory']
    search_fields = ['comment']
    date_hierarchy = 'date'

    class Media:
        js = (static('transactions/js/admin_dynamic_filters.js'),)
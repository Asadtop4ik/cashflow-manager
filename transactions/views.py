from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Subcategory

@staff_member_required
def filter_categories_by_type(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name') if type_id else []
    return JsonResponse(list(categories), safe=False)

@staff_member_required
def filter_subcategories_by_category(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name') if category_id else []
    return JsonResponse(list(subcategories), safe=False)
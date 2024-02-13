from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from .models import Category, Product

# Register your models here.


class CategoryFilter(admin.SimpleListFilter):
    """
    This is a custom filter for filtering products based on the category.

    You can check this link for more details;
    https://docs.djangoproject.com/en/5.0/ref/contrib/admin/filters/
    """
    # Human-readable title which will be displayed in the right admin sidebar
    # just above the filter options.
    title = _('By category')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value for the
        option that will appear in the URL query. The second element is the human-readable 
        name for the option that will appear in the right sidebar.
        """
        categories = Category.objects.all()

        # the code below can also be written as [(category.id, category.name) for category in categories]
        category_list = []

        for category in categories:
            category_tuple = (category.id, category.name)
            category_list.append(category_tuple)

        return category_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string
        and retrievable via `self.value()`.
        """
        if self.value():
            return queryset.filter(category__id__exact=self.value())

        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = [CategoryFilter, 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {
        'slug': ('name',)
    }

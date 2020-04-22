from django.contrib import admin
from .models import Category


# from .models import category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "number")
    list_filter = ("number",)

# Register your models here.

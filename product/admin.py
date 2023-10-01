from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class InformationAdmin(admin.StackedInline):
    model = models.Information


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    inlines = (InformationAdmin,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent', 'image_display')

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return None

    image_display.short_description = 'Image'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.FeaturedProducts)
class FeaturedProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'image_display')

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return None

    image_display.short_description = 'Image'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.OfferProducts)
class OfferProductsAdmin(admin.ModelAdmin):
    list_display = ('discount', 'total_price', 'price', 'image_display')

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return None

    image_display.short_description = 'Image'


@admin.register(models.Brande)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('product', 'brande', 'image_display')

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return None

    image_display.short_description = 'Image'


@admin.register(models.Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "body")


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Type)
admin.site.register(models.OrderItem)
admin.site.register(models.ProductImage)
admin.site.register(models.Like)

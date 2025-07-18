from adminsortable2.admin import SortableAdminBase, SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 0
    readonly_fields = ['get_preview']
    fieldsets = (
        (None, {
            'fields': ('image', 'get_preview', 'order')
        }),
    )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['place', 'get_preview']
    readonly_fields = ['get_preview']
    fieldsets = (
        (None, {
            'fields': ('place', 'image', 'get_preview')
        }),
    )

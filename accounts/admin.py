from django.contrib import admin
from .models import Profile
 
admin.site.register(Profile)

from django.contrib import admin
from orders.models import Order, OrderItem

from .models import ThemeSettings
 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'paid_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]

@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Colors", {
            "fields": (
                "background_default_color",
                "text_default_color",
                "action_primary_default_color",
                "action_secondary_default_color",
            )
        }),
    )

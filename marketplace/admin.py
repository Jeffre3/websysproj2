
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from .models import Purchase, Sale

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_repr', 'action_flag', 'change_message', 'action_time')
    readonly_fields = [f.name for f in LogEntry._meta.fields]
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 0
    readonly_fields = ('product', 'purchased_at')
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [PurchaseInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'purchased_at')
    readonly_fields = ('user', 'product', 'purchased_at')
    can_delete = False

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('seller', 'item_name', 'price', 'listed_at')
    readonly_fields = ('seller', 'item_name', 'price', 'listed_at')
    can_delete = False

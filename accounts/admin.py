from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Import BaseUserAdmin for extending
from.models import CustomUser
from.forms import UserRegistrationForm # Import custom form to use in admin for adding users

# Custom UserAdmin to show the 'role' and 'batch' fields in Django admin
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm # Use our custom registration form for adding users
    # The default change form is usually sufficient, but can be customized with CustomUserForm if needed.

    # Add 'role' and 'batch' to existing fieldsets for display/edit in admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'batch')}),
    )
    # Display 'role' and 'batch' in the user list view in admin
    list_display = BaseUserAdmin.list_display + ('role', 'batch')
    # Add 'role' to filters in admin list view
    list_filter = BaseUserAdmin.list_filter + ('role',)
    # Add 'batch' and 'email' to search fields
    search_fields = BaseUserAdmin.search_fields + ('batch', 'email')
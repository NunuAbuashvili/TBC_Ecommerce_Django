from django.contrib import admin

from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for CustomUser model.
    """
    add_form = CustomUserCreationForm
    list_display = (
        'username', 'email', 'date_of_birth', 'last_active_datetime'
    )
    list_filter = ('account_type', 'is_verified', 'is_active')
    search_fields = ('username', 'country')
    search_help_text = 'Search by username or country'
    ordering = ('date_of_birth',)

    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'password')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'gender', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Address', {
            'fields': ('country', 'city', 'street_address', 'postal_code')
        }),
        ('User Details', {
            'fields': (
                'date_joined', 'last_login', 'account_type',
                'is_verified', 'is_active', 'newsletter_subscription'
            )
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions', 'is_staff', 'is_superuser'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description="Address")
    def full_address(self, instance: CustomUser) -> str:
        """
        Returns the user's full address as a formatted string.

        Args:
            instance: The user instance.

        Returns:
            str: Formatted address string.
        """
        address_parts = [
            instance.street_address,
            instance.city,
            instance.postal_code,
            instance.country
        ]

        return ', '.join(filter(None, address_parts))

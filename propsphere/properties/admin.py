from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'price', 'address', 'user', 'created_at', 'updated_at')
    
    # Add filters for easy searching in the admin interface
    list_filter = ('user', 'created_at')
    
    # Enable search functionality
    search_fields = ('title', 'address', 'user__username')
    
    # Add fields for editing in the detail view
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'address', 'contact', 'image')
        }),
        ('Additional Information', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Make certain fields read-only in the admin interface
    readonly_fields = ('created_at', 'updated_at')

    # Allow image preview in the admin
    def image_tag(self, obj):
        if obj.image:
            return '<img src="{}" width="100" />'.format(obj.image.url)
        return ''
    image_tag.allow_tags = True
    image_tag.short_description = 'Image Preview'

    # Add the image preview field to the list_display
    list_display += ('image_tag',)

# Register the Property model with the custom admin
admin.site.register(Property, PropertyAdmin)

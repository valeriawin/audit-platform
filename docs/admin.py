from django.contrib import admin
from .models import Stock, DocsRequest

class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['client_id']}),
        ('Main information', {'fields': ['date'], 'classes': ['audit_file']}),
    ]
    list_display = ('client_id', 'date', 'status')
    list_filter = ['date']
    search_fields = ['client_id']

admin.site.register(DocsRequest, CompanyAdmin)
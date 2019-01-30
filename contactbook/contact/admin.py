from django.contrib import admin

# Register your models here.
from contact.models import ContactBook, Contact


class ContactBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'deleted']
    readonly_fields = ['id', 'created_on', 'created_by', 'changed_by', 'updated_on', 'deleted', 'deleted_on']
    list_filter = ('deleted',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'contact_book', 'deleted']
    readonly_fields = ['id', 'created_on', 'created_by', 'changed_by', 'updated_on', 'deleted', 'deleted_on']
    list_filter = ('deleted',)


admin.site.register(ContactBook, ContactBookAdmin)
admin.site.register(Contact, ContactAdmin)

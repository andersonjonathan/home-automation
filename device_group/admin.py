from django.contrib import admin

# Register your models here.
from .models import Group, GroupDeviceRelation


class GroupDeviceRelationAdmin(admin.TabularInline):
    model = GroupDeviceRelation


class GroupAdmin(admin.ModelAdmin):
    model = Group

    inlines = [GroupDeviceRelationAdmin]
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']

admin.site.register(Group, GroupAdmin)

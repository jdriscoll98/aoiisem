from django.contrib import admin
from House.models import House
from .forms import HouseForm

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    def House(self, obj):
        return obj.name

    list_display = ('House', 'manager')
    form = HouseForm
    fieldsets = (
        (None, {
            'fields': ('manager', 'name', 'primary_color',  'secondary_color')
            }),
        )

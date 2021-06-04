from django.contrib import admin
from .models import Room, Reservation, CheckIn, TypeService


class TypeServiceAdmin(admin.ModelAdmin):
    exclude = ("user",)
    readonly_fields = ("avg_rate",)


admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(CheckIn)
admin.site.register(TypeService, TypeServiceAdmin)

from django.contrib import admin
from .models import Room, Reservation, CheckIn, TypeService, UserTypeService


class TypeServiceAdmin(admin.ModelAdmin):
    exclude = ("user",)
    readonly_fields = ("avg_rate", "count_rate")


admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(CheckIn)
admin.site.register(TypeService, TypeServiceAdmin)
admin.site.register(UserTypeService)

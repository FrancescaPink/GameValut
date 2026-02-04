from django.contrib import admin
from .models import Event, EventRegistration

# La classe EventAdmin serve a personalizzare l'interfaccia di amministrazione per il modello Event
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_date', 'available_spots')
    list_filter = ('start_date',)
    search_fields = ('title', 'description')

admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
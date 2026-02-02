from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Thread, Post, Tag, Announcement, AnnouncementComment

# Configurazione personalizzata per vedere il campo "is_company" nella lista utenti
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_company', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Ruolo Personalizzato', {'fields': ('is_company',)}),
    )

# Registrazione dei modelli
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Announcement)
admin.site.register(AnnouncementComment)
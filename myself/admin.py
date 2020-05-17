from django.contrib import admin
from . import models
from django.forms import TextInput, Textarea
from django.db import models as django_db_models

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code','name')


class ContentAdmin(admin.ModelAdmin):
    list_display = ('name','language','title')
    list_filter = ('name','language')
    formfield_overrides = {
        django_db_models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        django_db_models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':80})},
    }



admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Content, ContentAdmin)

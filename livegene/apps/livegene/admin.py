from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.contrib.admin.widgets import AdminURLFieldWidget

from .models import SDG


class SDGAdmin(admin.ModelAdmin):
    list_display = ('headline', 'full_name')
    fields = ('headline', 'full_name', 'color', 'link', 'logo', 'logo_url')
    readonly_fields = ('logo',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'140'})},
        models.URLField: {'widget': AdminURLFieldWidget(
                                        attrs={'style': 'width: 40em'}
                                    )
                         },
    }


admin.site.register(SDG, SDGAdmin)

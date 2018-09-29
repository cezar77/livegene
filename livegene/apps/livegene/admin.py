from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.contrib.admin.widgets import AdminURLFieldWidget

from .models import (
    Project,
    Partnership,
    PartnershipRole,
    PartnershipRoleType,
    Person,
    PersonRole,
    ContactPerson,
    Country,
    CountryRole,
    SDG,
    SamplingActivity,
    SamplingDocumentType,
    SamplingDocument
)


class PartnershipRoleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    fields = ('id', 'description')
    readonly_fields = ('id',)


class PersonRoleAdmin(admin.ModelAdmin):
    fields = ('project', 'person', 'percent', 'total_percentage')
    readonly_fields = ('total_percentage',)


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


admin.site.register(Project)
admin.site.register(Partnership)
admin.site.register(PartnershipRole)
admin.site.register(PartnershipRoleType, PartnershipRoleTypeAdmin)
admin.site.register(Person)
admin.site.register(PersonRole, PersonRoleAdmin)
admin.site.register(ContactPerson)
admin.site.register(Country)
admin.site.register(CountryRole)
admin.site.register(SDG, SDGAdmin)
admin.site.register(SamplingDocumentType)
admin.site.register(SamplingActivity)
admin.site.register(SamplingDocument)

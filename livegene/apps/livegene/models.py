from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.html import format_html

from django_countries.fields import CountryField
from colorfield.fields import ColorField

from .validators import validate_lowercase


class ProjectManager(models.Model):
    def get_by_natural_key(self, ilri_code):
        return self.get(ilri_code=ilri_code)


class Project(models.Model):
    ilri_code = models.CharField(max_length=55, unique=True)
    full_name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=30, blank=True)
    principal_investigator = models.ForeignKey(
        'Person',
        on_delete=models.DO_NOTHING,
        related_name='projects'
    )
    group = models.CharField(max_length=55)
    #donor = models.ForeignKey(
    #    'Organisation',
    #    on_delete=models.DO_NOTHING,
    #    related_name='projects'
    #)
    donor_reference = models.CharField(max_length=55, blank=True)
    donor_project_name = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    capacity_development = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    objects = ProjectManager()

    class Meta:
        ordering = ('ilri_code',)

    def __str__(self):
        return '{0} ({1})'.format(self.full_name, self.ilri_code)

    def natural_key(self):
        return (self.ilri_code,)


class Partnership(models.Model):
    partner = models.ForeignKey(
        'Organisation',
        on_delete=models.DO_NOTHING,
        related_name='partnerships'
    )
    contact = models.ForeignKey(
        'Person',
        on_delete=models.DO_NOTHING,
        related_name='partnerships'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ('-end_date', '-start_date')
    

class PartnershipRole(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.DO_NOTHING,
        related_name='partnership_roles'
    )
    partnership = models.ForeignKey(
        'Partnership',
        on_delete=models.DO_NOTHING,
        related_name='roles'
    )
    role_type = models.ForeignKey(
        'PartnershipRoleType',
        on_delete=models.DO_NOTHING,
        related_name='roles'
    )

    class Meta:
        ordering = ('role_type',)


class PartnershipRoleType(models.Model):
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.description


class Organisation(models.Model):
    short_name = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    country = models.ForeignKey(
        'Country',
        on_delete=models.DO_NOTHING,
        related_name='organisations'
    )

    class Meta:
        ordering = ('full_name',)

    def __str__(self):
        return self.full_name


class PersonManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)


class Person(models.Model):
    username = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_lowercase]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    home_program = models.CharField(max_length=100)
    email = models.EmailField(validators=[validate_lowercase])

    objects = PersonManager()

    class Meta:
        verbose_name_plural = 'people'
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def natural_key(self):
        return (self.username,)


class PersonRole(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='person_roles'
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        related_name='roles'
    )
    percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('project', 'person')

    def __str__(self):
        return '{0} - {1}'.format(self.project, self.person)


class ContactPerson(models.Model):
    title = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, validators=[validate_lowercase])
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = 'contact people'
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.title:
            return '{0} {1} {2}'.format(
                self.title,
                self.first_name,
                self.last_name
            )
        else:
            return '{0} {1}'.format(self.first_name, self.last_name)


class CountryManager(models.Manager):
    def get_by_natural_key(self, country):
        return self.get(country=country)


class Country(models.Model):
    country = CountryField()

    objects = CountryManager()

    class Meta:
        verbose_name_plural = 'countries'
        ordering = ('country',)

    def __str__(self):
        return self.country.name

    def natural_key(self):
        return (self.country.country,)


class CountryRole(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='country_roles'
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE,
        related_name='roles'
    )
    percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('project', 'country')

    def __str__(self):
        return '{0} - {1}'.format(self.project, self.country)


class SDG(models.Model):
    """
    Sustainable Development Goals (SDG)
    More information under:
    https://en.wikipedia.org/wiki/Sustainable_Development_Goals
    """
    headline = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    color = ColorField()
    link = models.URLField(unique=True)
    logo_url = models.URLField(verbose_name='Logo URL', unique=True)

    class Meta:
        verbose_name = 'Sustainable Development Goal'
        verbose_name_plural = 'Sustainable Development Goals'
        ordering = ('pk',)

    def __str__(self):
        return self.headline

    @property
    def logo(self):
        return format_html(
            '<img src="{logo_url}" alt="{headline}">',
            logo_url=self.logo_url,
            headline=self.headline
        )


class SDGRole(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='sdg_roles'
    )
    sdg = models.ForeignKey(
        'SDG',
        on_delete=models.CASCADE,
        related_name='roles'
    )
    percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('project', 'sdg')

    def __str__(self):
        return '{0} - {1}'.format(self.project, self.sdg)


class SamplingActivity(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.DO_NOTHING,
        related_name='sampling_activities'
    )
    partnership = models.ForeignKey(
        'Partnership',
        on_delete=models.DO_NOTHING,
        related_name='sampling_activities'
    )
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = 'sampling activities'
        ordering = ('-end_date', '-start_date')

    def __str__(self):
        return self.description


class SamplingDocumentTypeManager(models.Manager):
    def get_by_natural_key(self, short_name):
        return self.get(short_name=short_name)


class SamplingDocumentType(models.Model):
    short_name = models.CharField(max_length=15)
    long_name = models.CharField(max_length=50)

    objects = SamplingDocumentTypeManager()

    class Meta:
        ordering = ('short_name', 'long_name')

    def __str__(self):
        return self.short_name

    def natural_key(self):
        return (self.short_name,)    


class SamplingDocument(models.Model):
    sampling_activity = models.ForeignKey(
        'SamplingActivity',
        on_delete=models.DO_NOTHING,
        related_name='sampling_documents'
    )
    document_type = models.ForeignKey(
        'SamplingDocumentType',
        on_delete=models.DO_NOTHING,
        related_name='sampling_documents'
    )
    document = models.FileField()

from django.db import models


class Expenditure(models.Model):
    ilri_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    home_program = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    report_date = models.DateField()
    total_budget = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        unique_together = ('ilri_code', 'report_date')

    def __str__(self):
        return self.name

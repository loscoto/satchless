from django import forms
from django.db import models
import decimal

from ..forms import variant_form_for_product, BaseVariantForm
from ..models import Product, Variant

#models for tests

class Parrot(Product):
    pass


class DeadParrot(Parrot):
    species = models.CharField(max_length=20)


class ZombieParrot(DeadParrot):
    pass


class ParrotVariant(Variant):
    pass


class Cheese(Product):
    quantity_quantizer = decimal.Decimal('0.01')


class CheeseVariant(Product):
    pass


class DeadParrotVariant(ParrotVariant):
    COLOR_CHOICES = (
        ('blue', 'blue'),
        ('white', 'white'),
        ('red', 'red'),
        ('green', 'green'),
    )
    product = models.ForeignKey(DeadParrot, related_name='variants')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    looks_alive = models.BooleanField()

    class Meta:
        unique_together = ('product', 'color', 'looks_alive')

    def __unicode__(self):
        "For debugging purposes"
        return u"%s %s %s" % (
                "alive" if self.looks_alive else "resting",
                self.get_color_display(), self.product.slug)


#@variant_form_for_product(DeadParrot)
class DeadParrotVariantForm(BaseVariantForm):
    color = forms.CharField(max_length=10)
    looks_alive = forms.BooleanField()

    def _get_variant_queryset(self):
        return DeadParrotVariant.objects.filter(product=self.product,
                                                color=self.cleaned_data['color'],
                                                looks_alive=self.cleaned_data['looks_alive'])

    def clean(self):
        if not self._get_variant_queryset().exists():
            raise forms.ValidationError("Variant does not exist")
        return self.cleaned_data

    def get_variant(self):
        return self._get_variant_queryset().get()


from satchless.product.tests.product import *
from satchless.product.tests.pricing import *

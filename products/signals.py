from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Product,AmazingOfferMain

import json


@receiver(m2m_changed, sender=AmazingOfferMain.products.through)
def offer_saver(sender, instance, **kwargs):
    for p in instance.products.all():
        p.off = instance.off
        p.save()


@receiver(m2m_changed, sender=Product.colors.through)
def generate_color_map(sender, instance , **kwargs):
    color_map_dict = {color.style_class : color.name for color in instance.colors.all()}        
    generated_json = json.dumps(color_map_dict)
    instance.colors_map = generated_json
    instance.save()

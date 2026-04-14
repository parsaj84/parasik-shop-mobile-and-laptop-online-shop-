from django.db.models.signals import m2m_changed,post_save
from django.dispatch import receiver


from .models import OffCode, Notfication, Order

@receiver(m2m_changed, sender=OffCode.users.through)
def notification_seter(sender, instance, **kwargs):
    if isinstance(instance, OffCode):
        for user in instance.users.all():                               
            if not Notfication.objects.filter(user=user, offcode=instance).exists():
                title = "کد تخفیف"
                text = f"کد تخفیف {instance.code} برای شما ثبت شد."
                notification = Notfication.objects.create(user=user, offcode=instance, type="OFC", title=title, text=text)

            


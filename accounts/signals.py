from django.db.models.signals import post_save
from accounts.models import NewUser, TestTransaction
from django.dispatch import receiver


@receiver(post_save, sender=NewUser)
def create_test_transaction(sender, instance, created, **kwargs):
    if created:
        print('created: ')
        if instance.is_staff:
            print('staff')
            return
        TestTransaction.objects.create(user=instance)
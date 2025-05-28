from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Faculty

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(user=instance)
        elif instance.is_faculty:
            Faculty.objects.create(user=instance)

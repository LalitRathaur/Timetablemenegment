from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Faculty, TimetableVote, TimetableCurrent, TimetableChange, Enrollment

# 1. Auto-create Student/Faculty Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(user=instance)
        elif instance.is_faculty:
            Faculty.objects.create(user=instance)

# 2. Auto-apply Timetable Change if approved
@receiver(post_save, sender=TimetableVote)
def apply_change_if_approved(sender, instance, **kwargs):
    change = instance.change

    if not change.applied and change.is_approved():
        cur_tt, created = TimetableCurrent.objects.get_or_create(date=change.date)
        slot_attr = f"slot{change.slot_number}"

        if change.status == 'cancelled':
            setattr(cur_tt, slot_attr, "")
        elif change.status == 'added':
            setattr(cur_tt, slot_attr, change.course_code)

        cur_tt.save()

        change.applied = True
        change.save()

from django.contrib import admin
from .models import User, Student, Faculty, Course, Enrollment, TimetableMain, TimetableCurrent, TimetableChange, TimetableVote
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_faculty')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(TimetableMain)
admin.site.register(TimetableCurrent)
admin.site.register(TimetableChange)
admin.site.register(TimetableVote)
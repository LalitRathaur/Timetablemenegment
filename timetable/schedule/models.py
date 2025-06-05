from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)


# Student profile
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


# Faculty profile
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"


# Course offered by faculty
class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.course_code} - {self.name}"


# Enrollment model
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} -> {self.course.course_code}"


# Main Timetable (default structure)
class TimetableMain(models.Model):
    day = models.CharField(max_length=10)  # e.g., Monday, Tuesday
    slot1 = models.CharField(max_length=50)
    slot2 = models.CharField(max_length=50)
    slot3 = models.CharField(max_length=50)
    slot4 = models.CharField(max_length=50)
    slot5 = models.CharField(max_length=50)
    slot6 = models.CharField(max_length=50)

    def __str__(self):
        return f"Main Timetable - {self.day}"


# Current Timetable (copied from main but editable)
class TimetableCurrent(models.Model):
    date = models.DateField(unique=True)
    slot1 = models.CharField(max_length=50)
    slot2 = models.CharField(max_length=50)
    slot3 = models.CharField(max_length=50)
    slot4 = models.CharField(max_length=50)
    slot5 = models.CharField(max_length=50)
    slot6 = models.CharField(max_length=50)

    def __str__(self):
        return f"Timetable for {self.date}"


# Timetable Change Proposal (added/cancelled)
class TimetableChange(models.Model):
    STATUS_CHOICES = [
        ('added', 'Added'),
        ('cancelled', 'Cancelled'),
    ]

    date = models.DateField()
    slot_number = models.PositiveSmallIntegerField(choices=[(i, f"Slot {i}") for i in range(1, 7)])
    course_code = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('date', 'slot_number')

    def __str__(self):
        return f"{self.date} - Slot {self.slot_number} - {self.course_code} ({self.status})"

    @property
    def vote_count(self):
        return self.votes.count()

    def is_approved(self):
        from django.db.models import Count
        enrolled_count = Enrollment.objects.filter(course__course_code=self.course_code).count()
        return self.vote_count > (enrolled_count / 2)


# Voting Model
class TimetableVote(models.Model):
    change = models.ForeignKey(TimetableChange, on_delete=models.CASCADE, related_name='votes')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('change', 'student')  # ensures one vote per student per change

    def __str__(self):
        return f"{self.student.user.username} voted on {self.change}"

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegisterForm, EnrollmentForm, VoteForm
from .models import User, Student, Faculty, Enrollment, TimetableChange, TimetableVote
from django.http import HttpResponse
# Register User and create profile
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = form.cleaned_data.get('is_student')
            user.is_faculty = form.cleaned_data.get('is_faculty')
            user.save()  # this will trigger signal
            login(request, user)
            return HttpResponse("User registered successfully.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def create_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enrollment_list')  # list or any page
    else:
        form = EnrollmentForm()
    return render(request, 'enrollment_form.html', {'form': form})

# Cast a vote for a timetable change
def cast_vote(request, change_id):
    change = get_object_or_404(TimetableChange, pk=change_id)
    user = request.user

    # Check if user is enrolled in the course related to this change
    if not Enrollment.objects.filter(student__user=user, course__course_code=change.course_code).exists():
        return render(request, 'error.html', {'message': "You are not enrolled in this course to vote."})

    # Check if user already voted
    if TimetableVote.objects.filter(change=change, voter=user).exists():
        return render(request, 'error.html', {'message': "You have already voted on this change."})

    if request.method == 'POST':
        vote = TimetableVote.objects.create(change=change, voter=user)
        vote.save()
        # The signal will handle applying change if votes > half
        return redirect('change_detail', change_id=change.id)

    return render(request, 'vote_confirm.html', {'change': change})

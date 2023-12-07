from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, CourseForm, BlogForm
from .models import Course, Blog, About, Testimonial, Supporter, Comment,CustomUser, Review, Enrollment, Receipt, Payment, GuestMessage, Notification
from django.http import JsonResponse
from django.contrib import messages
import datetime

# -- function for registration, login, authorixzation--
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'
            user.save()
            login(request, user)
            return redirect('login_view')  
    else:
        form = RegistrationForm()
    about_data= About.objects.all()
    return render(request, 'register.html', {'form': form, 'about_data': about_data})

def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'instructor':
                return redirect('instructor') 
            elif user.user_type == 'student':
                return redirect('student') 
            else:
                return redirect('index')  

        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    about_data= About.objects.all()
    return render(request, 'login.html', {'about_data': about_data})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def instructor(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
    courses = Course.objects.filter(user=user)
    blog = Blog.objects.filter(user=user)

    user_type = user.user_type
    profile_photo = user.profile_photo
    bio = user.bio
    username = user.username

    context = {
        'user': user,
        'user_type': user_type,
        'profile_photo': profile_photo,
        'bio': bio,
        'username': username,
        'notifications': notifications,
        'courses': courses,
        'blog': blog

    }
    return render(request, 'dashboard_instructor.html', context)

@login_required
def student(request):
    user = request.user
    about_data = About.objects.all()
    return render(request, 'student.html', {'about_data': about_data})

# -- End of register, login, authentication function --


# -- Start of course function --
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user  
            course.save()
            return redirect('instructor')  
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})

def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructor = CustomUser.objects.filter(user_type='instructor')
    reviews = Review.objects.filter(course=course)
    about_data = About.objects.all()
    return render(request, 'course-detail.html', {'course': course,'instructor': instructor, 'review': reviews, 'about_data': about_data})

def view_all_course(request):
    course = Course.objects.all()
    return render(request, 'courses.html', {'course': course})

# -- End of course function --


# -- Start of blog function --
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
           
            new_blog = form.save(commit=False)
            new_blog.user = request.user  
            new_blog.save()
            return redirect('blog_list')  
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})

def blog(request, key):
    B = Blog.objects.get(id=key)
    blog_cmnt = Comment.objects.filter(blog=B, parent_comment=None)
    recent_blogs = Blog.objects.exclude(id=key)

    if request.method == 'POST':
        email = request.POST['email']
        comments = request.POST['comments']
        parent_comment_id = request.POST.get('parent_comment')  

        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            cmnt = Comment(
                blog=B,
                email=email,
                comments=comments,
                parent_comment=parent_comment  
            )
        else:
            cmnt = Comment(
                blog=B,
                email=email,
                comments=comments,
                parent_comment=None
            )

        cmnt.save()

        for comment in blog_cmnt:
           comment.replies = Comment.objects.filter(parent_comment=comment)

    return render(request, 'blog-single.html', {'B': B, 'comments': blog_cmnt, 'recent_blogs': recent_blogs })


def view_all_blog(request):
    blog = Blog.objects.all()
    return render (request, 'blog-grid.html', {'blog': blog})

# -- End of blog function --

# -- start of review function --

def add_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        course_id = request.POST.get('course_id')  
        
        course = Course.objects.get(pk=course_id)
        review = Review(course=course, name=name, email=email, text=text)
        review.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# -- End of review function --

# --Start of the enroll, payment function --

def enroll_course(request, course_id):

    if not request.user.is_authenticated:
        return redirect('register')
    
    course = Course.objects.get(pk=course_id)
    enrollment_exists = Enrollment.objects.filter(user=request.user, course=course).exists()

    Notification.objects.create(
        recipient=request.user,
        course=course,
        message=f'You have joined the course "{course.title}".'
        )  

    if enrollment_exists:
        messages.error(request, 'You are already enrolled in this course.')
        return redirect('course_detail', course_id=course_id)

    return render(request, 'enroll_course.html', {'course': course})

def payment_process(request, course_id):
    if request.method == "POST":
       #api halne thau
       
        payment = Payment.objects.create(
            user=request.user,
            payment_status="Success",  
            date=datetime.date.today(),  
            receipt=None,  
            payment_method="Credit Card"  
        )
        
        receipt = Receipt.objects.create(
            receipt_date=datetime.date.today()  
        )
        
        enrollment = Enrollment.objects.get(user=request.user, course_id=course_id)
        enrollment.pay_status = True
        enrollment.pay_date = datetime.date.today()  
        enrollment.save()
        
        messages.success(request, "Payment successful! You are now enrolled.")
        return redirect('payment_success', receipt_id=receipt.pk)  
        
    return render(request, 'payment_failure.html')

def payment_success(request):
    return render(request, 'payment-success.html')

# -- End of enroll, payment function --

# -- Start of contact function --

def contact_form(request):
    about_data = About.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        guest_message = GuestMessage(name=name, email=email, subject=subject, message=message)
        guest_message.save()

        success_message = "Your message has been sent successfully."
        return JsonResponse({'success_message': success_message})

    return render(request, 'contact.html', {'about_data': about_data})

# -- End of contact function --

# -- start of get_data function --
def get_data(request):
    about_data = About.objects.all()
    cr = Course.objects.all()
    bl = Blog.objects.all()
    testi = Testimonial.objects.all()
    sup = Supporter.objects.all()

    context ={
        'about_data': about_data,
        'cr': cr,
        'bl': bl,
        'testi': testi,
        'sup': sup,
    }
    
    return render(request, 'index.html', context)

# -- End of get_data function --
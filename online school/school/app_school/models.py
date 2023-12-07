from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # Add other custom fields as needed

    def __str__(self):
        return self.username
    
class About(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    facebook_link = models.URLField()
    insta_link = models.URLField()
    x_link = models.URLField()


# Course Model
class Course(models.Model):
    LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advance', 'Advance'),
    ]
    
    CATEGORY_CHOICES = [
        ('UI/UX Design', 'UI/UX Design'),
        ('Data Science', 'Data Science'),
        ('Development', 'Development'),
        ('Business', 'Business'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Design', 'Design'),
    ]
    
    photo = models.ImageField(upload_to='course_photos/', default=False)
    title = models.CharField(max_length=100)
    content = models.TextField()  
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    language = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    certificate = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return f"Review by {self.name} for Course: {self.course.title}"



# Testimonial Model
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonial_photos/')
    message = models.TextField()

# Supporter Model
class Supporter(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='supporter_logos/')

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='blog/')
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Comment Model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    email = models.EmailField()
    comments = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

# Guest Message Model
class GuestMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

# Enrollment Model
class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pay_status = models.BooleanField(default=False)
    pay_date = models.DateField()

# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20)
    date = models.DateField()
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)

# Receipt Model
class Receipt(models.Model):
    payment_id = models.AutoField(primary_key=True)
    receipt_date = models.DateField()


class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    timestamp = models.DateTimeField(auto_now_add=True)

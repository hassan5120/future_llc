from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Contact
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Review
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout

def home(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    return render(request, 'axit.html', {'first_letter':first_letter})

def about(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    return render(request, 'about.html', {'first_letter':first_letter})

def services(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    return render(request, 'services.html', {'first_letter':first_letter})

def specialities(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    return render(request, 'specialities.html', {'first_letter':first_letter})

def softwares(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    return render(request, 'softwares.html', {'first_letter':first_letter})

def testimonials(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    reviews = Review.objects.all()
    return render(request, 'testimonials.html', {'first_letter':first_letter, 'reviews':reviews})

def contact(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        
        from_email = settings.EMAIL_HOST_USER
        message_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
        
        send_mail(
            subject=f"New Contact: {subject}",
            message=message_body,
            from_email=from_email,
            recipient_list=[from_email],
            fail_silently=False,
        )
        
        messages.success(request, 'Contact Form Successfully submitted')

        return redirect('/contact')

    return render(request, 'contact.html', {'first_letter':first_letter})

def send_email(request):
    recipient_email = 'ahsanqamar2021@gmail.com'
    send_mail(
        subject='New Contact: Example Subject',
        message="This is a test message.",
        from_email='futuresigns9098@gmail.com',
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    return HttpResponse("Email sent successfully")






def submit_review(request):
    if request.method == 'POST':
        name = request.POST.get('rev-name')
        email = request.POST.get('rev-email')
        review_text = request.POST.get('rev-text')
        field_name = request.POST.get('rev-field')
        image = request.FILES.get('rev-image')
        
        review = Review(name=name, email=email, review_text=review_text, field_name=field_name, image=image)
        if len(review_text)>=200:
            messages.warning(request, 'Characters should be less than 200')
            return redirect('/testimonials')
        else:
             review.save()
        
        from_email = settings.EMAIL_HOST_USER
        message_body = f"Name: {name}\nEmail: {email}\nField: {field_name}\nReview: {review_text}"
        
        send_mail(
            subject=f"New Review by {name}",
            message=message_body,
            from_email=from_email,
            recipient_list=[from_email],
            fail_silently=False,
        )
        
        messages.success(request, 'Review Successfully submitted')
        return redirect('/testimonials')
        
        # return JsonResponse({'message': 'Review submitted successfully'})

    # Handle GET requests or other cases as needed
    # return JsonResponse({'message': 'Invalid request'})

def register(request):
    if request.method == 'POST':
        registerfname = request.POST['registerfname']
        registerlname = request.POST['registerlname']
        registerusername = request.POST['registerusername']
        registeremail = request.POST['registeremail']
        registerpassword = request.POST['registerpassword']
        confirmpassword = request.POST['cpassword']
        if registerpassword == confirmpassword:
            if User.objects.filter(email=registeremail).exists():
                messages.warning(
                    request, 'This email address is already in use.')
                return redirect('register')
            else:
                register = User.objects.create_user(
                    registerusername, registeremail, registerpassword)
                register.first_name = registerfname
                register.last_name = registerlname
                register.save()
                from_email = settings.EMAIL_HOST_USER
                
                # Mail to Admin
                
                message_body = f"Name: {registerfname} {registerlname}\nEmail: {registeremail}\nUsername: {registerusername}"
                
                send_mail(
                    subject=f"New Registeration by {registerfname}",
                    message=message_body,
                    from_email=from_email,
                    recipient_list=[from_email],
                    fail_silently=False,
                )
                
                # Mail to User
                
                message_body = f"Thank you {registerfname} {registerlname} for registering on our site.\nBest regards,\n Future Sign llc Team"
                
                send_mail(
                    subject= "Welcome to Our Website!",
                    message=message_body,
                    from_email=from_email,
                    recipient_list=[registeremail],
                    fail_silently=False,
                )
                messages.success(
                    request, 'Registration successful.')
                return redirect('/')
        else:
            messages.warning(request, 'Passwords do not match.')
            return redirect('/')
    else:
       return redirect('/')

def loginuser(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        loginn = authenticate(username=loginusername, password=loginpassword)
        if loginn is not None:
            login(request, loginn)
            messages.success(request, f'SuccessFully Login {request.user.username}')
            
            # Mail to User
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%B %d, %Y %I:%M %p")
            from_email = settings.EMAIL_HOST_USER
            message_body = f'''
            Hello,\n

            This is a notification to let you know that a login has been recorded for your Future Sign llc account.\n

            Date and Time of Login: {formatted_datetime}\n

            If you did not initiate this login or believe it to be unauthorized, please take immediate action to secure your account.\n

            Best regards,\n
            Future Sign llc Team
            '''
                
            send_mail(
                    subject= "Login Alert",
                    message=message_body,
                    from_email=from_email,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )
            return redirect('/')
        else:
            messages.warning(request, 'invalid Credentials')
            return redirect('/')
    else:
        return redirect('/')

def logoutuser(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/')

def profile(request):
    first_letter=''
    if request.user.is_authenticated:
        username = request.user.username
        first_letter = username[0]
        return render(request, 'profile.html', {'first_letter':first_letter})
    else:
        messages.warning(request, 'Please Login First')
        return redirect('/')


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profilefname = request.POST.get('profilefname')
            profilelname = request.POST.get('profilelname')
            profileemail = request.POST.get('profileemail')
            profilepassword = request.POST.get('profilepassword')

            if profilefname:
                request.user.first_name = profilefname
            if profilelname:
                request.user.last_name = profilelname
            if profileemail:
                if User.objects.exclude(pk=request.user.pk).filter(email=profileemail).exists():
                    messages.warning(request, 'This email address is already in use.')
                    return redirect('/profile')
                request.user.email = profileemail
            if profilepassword:
                request.user.set_password(profilepassword)
                login(request, request.user)

            request.user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('/profile')
    else:
        messages.error(request, 'Please Login First')
        return redirect('/')
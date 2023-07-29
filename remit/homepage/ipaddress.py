# In your app's models.py file
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def log_user_login(request, user, **kwargs):
    return str(request.META['REMOTE_ADDR'])
    print(f"User {user.username} logged in from IP: {request.META['REMOTE_ADDR']}")

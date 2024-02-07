from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from app import settings

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError("User must have an email address")
        
        email = self.normalize_email(email) # lowercase the right half of the email from the'@mail.com'
        user = self.model(email=email, name=name) # create the model object

        user.set_password(password) # save the password with encryption
        user.save(using=self.db) # save the object in the database

        return user
    
    def create_superuser(self, email, name, password):
        """Create a new superuser with the given details"""
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Databse model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Retrieve string representation of the user"""
        return self.email
    

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feed')
    status_text = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the ProfileFeedItem"""
        return self.status_text
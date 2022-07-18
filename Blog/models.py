from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class CustomUser(AbstractUser):
    HOD = '1'
    STAFF = '2'
    STUDENT = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'staff': STAFF,
        'student': STUDENT
    }

    user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Client"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    profile_pic = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.username


class Blog(models.Model):
    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    sumary = models.CharField(max_length=150)
    image  = models.ImageField(null=True, blank=True)
    body = models.CharField(max_length=1500)


class Comment(models.Model):
    author = models.ForeignKey(Client, models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Client.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.client.save()

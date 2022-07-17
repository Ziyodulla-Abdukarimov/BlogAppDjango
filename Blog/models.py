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
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='staff')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)


class Client(models.Model):
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='client')
    id = models.AutoField(primary_key=True)
    point = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-point', 'date')

    def __str__(self):
        return self.admin.username



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

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.apps import apps
# Create your models here.



class User(AbstractUser):
    ROLE_CHOICES = [
        ('STUDENT', 'Etudiant'),
        ('PROFESSOR', 'Professeur'),
        ('STAFF', 'Personnel Administratif'),
        ('SUPERVISOR', 'Surveillant'),
    ]
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
    ]
    profile_photo=models.ImageField(verbose_name='Photo de profil')
    date_naissance=models.DateField(verbose_name='Date de naissance')
    lieu_naissance=models.CharField(max_length='30',verbose_name='Lieu de naissance')
    genre=models.CharField(max_length=1,choices=GENDER_CHOICES,verbose_name='Sexe')
    role=models.CharField(max_length=30,choices=ROLE_CHOICES,verbose_name='Rôle')
    tel_number=PhoneNumberField(verbose_name='Numéro de téléphone')


    def set_role(self):
        Group=apps.get_model('auth','Group')
        students=Group.objects.get(name='students')
        professors=Group.objects.get(name='professors')
        staff=Group.objects.get(name='staff')
        Student = apps.get_model('backend', 'Student')
        Professor = apps.get_model('backend', 'Professor')
        Staff = apps.get_model('backend', 'Staff')
        if isinstance(self, Student):
            self.role = self.ROLE_CHOICES[0][0]
            students.user_set.add(self)
        elif isinstance(self, Professor):
            self.role = self.ROLE_CHOICES[1][0]
            professors.user_set.add(self)
        elif isinstance(self, Staff):
            self.role = self.ROLE_CHOICES[2][0]
            staff.user_set.add(self)


    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.set_role()

        def __str__(self):
            return f'{self.first_name} {self.last_name}'



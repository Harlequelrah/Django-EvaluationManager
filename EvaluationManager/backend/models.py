from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
# from backend.models import User

class Salle(models.Model):
    nom=models.CharField(null=True,max_length=25)
    is_free=models.BooleanField(default=True)
    capacite=models.IntegerField()
    def __str__(self):
        return f'{self.nom})'

class Filiere(models.Model):
    nom=models.CharField(null=True,max_length=25)
    description=models.CharField(null=True,max_length=50)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return f'{self.nom})'

class Student(User):
    CURSUS_CHOICES = [
        ('L', 'Licence'),
        ('M', 'Master'),
        ('D', 'Doctorat'),
        ('B', 'BTS'),
        ('P', 'Cours Preparatoire'),

    ]
    cursus = models.CharField(max_length=1, choices=CURSUS_CHOICES)
    filiere = models.ForeignKey(Filiere, on_delete=models.DO_NOTHING)
    salle = models.ForeignKey(Salle, on_delete=models.DO_NOTHING)

class Faculty(User):
    def supervise(self):
        Group = apps.get_model('auth', 'Group')
        supervisors = Group.objects.get(name='supervisors')
        self.role = self.ROLE_CHOICES[3][0]
        supervisors.User_set.add(self)

    def unsupervise(self):
        Group = apps.get_model('auth', 'Group')
        supervisors = Group.objects.get(name='supervisors')
        self.role = self.ROLE_CHOICES[3][0]
        supervisors.User_set.remove(self)


class Professor(Faculty):
    is_intern=models.BooleanField(default=True)
    epreuves=models.ManyToManyField('Epreuve',related_name='epreuves_soumis')

class Staff(Faculty):
    grade=models.CharField(max_length=30)

class Epreuve(models.Model):
    cours=models.ForeignKey('Cours',on_delete=models.DO_NOTHING)
    salle=models.ForeignKey(Salle,on_delete=models.DO_NOTHING)
    filiere=models.ForeignKey(Filiere,on_delete=models.DO_NOTHING)
    date=models.DateField()
    debut=models.DateTimeField()
    fin=models.DateTimeField(null=True)
    professeurs = models.ManyToManyField(Professor, related_name='professeur_soummeteur')
    surveillants = models.ManyToManyField(
        Faculty,
        limit_choices_to={'role__in': ['PROFESSOR', 'STAFF']},
        related_name='epreuves_supervisees'
    )
    def get_start_time(self):
        return self.debut.strftime('%H:%M')
    def get_end_time(self):
        return self.fin.strftime('%H:%M')

    def __str__(self):
        return f'Epreuve de {self.cours.nom})'

class Cours(models.Model):
    nom=models.CharField(max_length=30)
    professeurs = models.ManyToManyField(Professor, related_name='cours_enseignes')
    def __str__(self):
        return f'{self.nom})'

class Evalutation(models.Model):
    EXAMS_TYPES = [
        ('Assignment', 'Devoir'),
        ('EXAM', 'Partiel'),
        ('Project', 'Projet'),
        ('Presentation', 'Présentation'),
    ]
    type_evaluation=models.CharField(max_length=20,choices=EXAMS_TYPES)
    date_debut=models.DateField()
    date_fin=models.DateField()
    epreuves = models.ManyToManyField('Epreuve', related_name='evaluations')
    def __str__(self):
        return f'{self.type_evaluation} du {self.date_debut} au {self.date_fin}'





class Note(models.Model):
    student=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    epreuve=models.ForeignKey(Epreuve , on_delete=models.DO_NOTHING)
    note=models.FloatField()
    def __str__(self):
        return f'{self.note}/ 20)'

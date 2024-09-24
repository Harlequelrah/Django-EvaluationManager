from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils import timezone
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

class Classe(models.Model):
    CURSUS_CHOICES = [
        ('L', 'Licence'),
        ('M', 'Master'),
        ('D', 'Doctorat'),
        ('B', 'BTS'),
        ('P', 'Cours Preparatoire'),
    ]
    LVL_CHOICES = [
        ('1', '1 er  Année'),
        ('2', '2 eme Année'),
        ('3', '3 eme Année'),
        ('4', '4 eme Année'),
        ('5', '5 eme Année'),
        ('6','6 eme Année'),
    ]
    cursus = models.CharField(max_length=1, choices=CURSUS_CHOICES)
    filiere = models.ForeignKey(Filiere, on_delete=models.DO_NOTHING)
    salle = models.ForeignKey(Salle, on_delete=models.DO_NOTHING)
    niveau=models.CharField(max_length=10,choices=LVL_CHOICES)
    annee_academique = models.CharField(max_length=9, verbose_name='Année académique', null=True, blank=True)


    def __str__(self):
        return f'{self.cursus}{self.niveau} - Salle {self.salle}'


class Student(User):
    classe=models.ForeignKey(Classe, on_delete=models.DO_NOTHING)
    matricule = models.CharField(max_length=20, verbose_name='Matricule', null=True, blank=True)


    def save(self,*args,**kwargs):
        if self.matricule and not self.annee_scolaire:
            current_year = timezone.now.year()
            self.annee_scolaire = f"{current_year}-{current_year+1}"
        super.save(*args, **kwargs)


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

    class Meta:
        abstract=True


class Professor(Faculty):
    is_intern=models.BooleanField(default=True)
    epreuves=models.ManyToManyField('Epreuve',related_name='epreuves_soumis')

class Staff(Faculty):
    poste=models.CharField(max_length=30)

class Epreuve(models.Model):
    cours=models.ForeignKey('Cours',on_delete=models.DO_NOTHING)
    classe=models.ForeignKey('Classe',on_delete=models.DO_NOTHING)
    date=models.DateField()
    debut=models.DateTimeField()
    fin=models.DateTimeField(null=True)
    professeurs = models.ManyToManyField(Professor, related_name='professeur_soummeteur')
    surveillants = models.ManyToManyField(
        User,
        limit_choices_to={'faculty__role__in': ['PROFESSOR', 'STAFF']},
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

class Evaluation(models.Model):
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

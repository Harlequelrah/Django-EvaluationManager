from django.contrib import admin

# Register your models here.
from .models import *

class SalleAdmin(admin.ModelAdmin):
    list_display=('nom','is_free','capacite')
    search_fields=('nom','is_free','capacite')

class FiliereAdmin(admin.ModelAdmin):
    list_display=('nom','is_active','description')
    search_fields=('nom','is_active','description')

class StaffAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','poste')
    search_fields=('first_name','last_name','poste')

class ProfessorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','is_intern')
    search_fields=('first_name','last_name','is_intern')


class StudentAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','classe','matricule')
    search_fields=('first_name','last_name','classe')

class EpreuveAdmin(admin.ModelAdmin):
    list_display=('cours','date','classe')
    search_fields=('cours','date','classe')

class CoursAdmin(admin.ModelAdmin):
    list_display=('nom')
    search_fields=('nom')

class NoteAdmin(admin.ModelAdmin):
    list_display=('cours','epreuve','note')
    search_fields=('cours','epreuve','note')

class Evaluationdmin(admin.ModelAdmin):
    list_display=('type_evaluation','date_debut','date_fin')
    search_fields=('type_evaluation','date_debut','date_fin')


# Register your models here.
admin.site.register(Filiere, FiliereAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Salle,SalleAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Epreuve, EpreuveAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Cours,CoursAdmin)
admin.site.register(Evaluation,Evaluationdmin)

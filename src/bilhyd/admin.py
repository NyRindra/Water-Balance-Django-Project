from django.contrib import admin

from bilhyd.models import Faculty, Campus, Cursus, Employee, Job, Student, Message, Genre

admin.site.register(Faculty)
admin.site.register(Campus)
admin.site.register(Cursus)
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(Student)
admin.site.register(Message)
admin.site.register(Genre)
#   Nous avons omis la classe Person parce que nous allons toujours
#   creer seulement soit un etudiant soit un employé directement (les classes filles qui seulement donnent naissance
#   à des veritable objet)

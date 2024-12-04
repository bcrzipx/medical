from django.contrib import admin
from .models import Rendezvous, Malade,Consultation,Ordonnance

# Register your models here.
admin.site.register(Rendezvous)
admin.site.register(Malade)
admin.site.register(Consultation)
admin.site.register(Ordonnance)
admin.site.site_header="Dr Asmaa Abidine"
admin.site.site_title="Dr Asmaa Abidine"

from django.contrib import admin
from .models import Rendezvous, Malade, Consultation, Ordonnance


@admin.register(Malade)
class MaladeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'sexe', 'date_naissance')
    list_filter = ('sexe', 'date_naissance')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    ordering = ('nom', 'prenom')
    readonly_fields = ()  # Pas de champs en lecture seule pour Malade


@admin.register(Rendezvous)
class RendezvousAdmin(admin.ModelAdmin):
    list_display = ('malade', 'date', 'heure', 'raison', 'get_patient_email')
    list_filter = ('date', 'heure')
    search_fields = ('malade__nom', 'malade__prenom', 'malade__email', 'raison')
    date_hierarchy = 'date'
    ordering = ('-date', '-heure')
    
    def get_patient_email(self, obj):
        return obj.malade.email
    get_patient_email.short_description = 'Email du patient'


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('rendezvous', 'date', 'heure', 'poids', 'tension', 'fievre', 'get_patient_name')
    list_filter = ('date',)
    search_fields = ('rendezvous__malade__nom', 'rendezvous__malade__prenom')
    date_hierarchy = 'date'
    ordering = ('-date', '-heure')
    fieldsets = (
        ('Informations générales', {
            'fields': ('rendezvous', 'date', 'heure', 'raison')
        }),
        ('Examens', {
            'fields': ('etat_hydrodynamique', 'etat_respiratoire', 'echographie')
        }),
        ('Mesures', {
            'fields': ('poids', 'tension', 'fievre')
        }),
    )
    
    def get_patient_name(self, obj):
        return f"{obj.rendezvous.malade.prenom} {obj.rendezvous.malade.nom}"
    get_patient_name.short_description = 'Patient'


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'date', 'heure', 'get_patient_name')
    list_filter = ('date',)
    search_fields = ('consultation__rendezvous__malade__nom', 'consultation__rendezvous__malade__prenom', 'contenue')
    date_hierarchy = 'date'
    ordering = ('-date', '-heure')
    
    def get_patient_name(self, obj):
        return f"{obj.consultation.rendezvous.malade.prenom} {obj.consultation.rendezvous.malade.nom}"
    get_patient_name.short_description = 'Patient'


# Configuration de l'admin
admin.site.site_header = "Dr Asmaa Abidine - Administration"
admin.site.site_title = "Dr Asmaa Abidine"
admin.site.index_title = "Gestion du Cabinet Médical"

from jp.models import *
from django.contrib import admin

class RainbowEntryAdmin(admin.ModelAdmin):
    list_display = ('base', 'added')
    search_fields = ['base', 'added']
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'preferred_project')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name')
    
class InputDataAdmin(admin.ModelAdmin):
    list_display = ('input_data_id', 'project', 'num_dealt')
    
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'input_data')
    
admin.site.register(RainbowEntry, RainbowEntryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(InputData, InputDataAdmin)
admin.site.register(Job, JobAdmin)
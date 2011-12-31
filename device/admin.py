from device.models import Device, Promoter, RBS, Protein, Terminator
from django.contrib import admin

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'promoter', 'rbs', 'protein', 'terminator')

class PromoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'sequence', 'external_URL', 'induced_by', 'repressed_by', 'PoPS')

class RBSAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'sequence', 'external_URL', 'RiPS')

class TerminatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'sequence', 'external_URL', 'fwd_efficiency', 'rev_efficiency')

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'sequence', 'external_URL', 'protein_output')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Promoter, PromoterAdmin)
admin.site.register(RBS, RBSAdmin)
admin.site.register(Terminator, TerminatorAdmin)
admin.site.register(Protein, ProteinAdmin)

from bench.models import Bench, Promoter, RBS, Protein, Terminator
from django.contrib import admin

class BenchAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'desc', 'author', 'challenge')
    prepopulated_fields = {'slug': ('name',)}

class PromoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence', 'url', 'PoPS')

class RBSAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence', 'url', 'RiPS')

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence', 'url', 'proteinOutput')

class TerminatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence', 'url', 'efficiency', 'forward')

    
admin.site.register(Bench, BenchAdmin)
admin.site.register(Promoter, PromoterAdmin)
admin.site.register(RBS, RBSAdmin)
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Terminator, TerminatorAdmin)
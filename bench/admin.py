from bench.models import Bench
from django.contrib import admin

class BenchAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'desc', 'author', 'challenge')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Bench, BenchAdmin)

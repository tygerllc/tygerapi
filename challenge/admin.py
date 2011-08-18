from challenge.models import Challenge, Criteria
from django.contrib import admin

class CriteriaInline(admin.TabularInline):
	model = Criteria
	extra = 2

class ChallengeAdmin(admin.ModelAdmin):
	list_display = ('name', 'points', 'bounty', 'bounty_avail')
	fieldsets = [
        	('General',               {'fields': ['name', 'create_date']}),
            ('Description',               {'fields': ['descrip']}),
        	('Rewards', {'fields': ['points', 'bounty']}),
    ]
	inlines = [CriteriaInline]
	search_fields = ['name']

admin.site.register(Challenge, ChallengeAdmin)
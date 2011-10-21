from challenge.models import Challenge, Criteria, UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

class CriteriaInline(admin.TabularInline):
    model = Criteria
    extra = 2

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'votes', 'bounty', 'bounty_avail')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = [
        ('General', {'fields': ['name', 'slug', 'tags', 'descrip', 'sponsor']}),
        ('Rewards', {'fields': ['votes', 'bounty']})
    ]
    inlines = [CriteriaInline]
    search_fields = ['name']

admin.site.register(User, UserProfileAdmin)
admin.site.register(Challenge, ChallengeAdmin)
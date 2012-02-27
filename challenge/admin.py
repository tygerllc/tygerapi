from challenge.models import Challenge, Criteria, UserProfile, Useful_Component, Useful_Link, Environment, SourceSink
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

class ComponentInline(admin.TabularInline):
    model = Useful_Component

class RefInline(admin.TabularInline):
    model = Useful_Link

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'votes', 'bounty', 'bounty_avail')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = [
        ('General', {'fields': ['name', 'image', 'slug', 'tags', 'sponsor']}),
        ('Description', {'fields': ['descrip',]}),
        ('Rewards', {'fields': ['votes', 'bounty']})
    ]
    inlines = [CriteriaInline, ComponentInline, RefInline,]

class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'temp', 'pH')

class SourceSinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')

admin.site.register(User, UserProfileAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(SourceSink, SourceSinkAdmin)
admin.site.register(Challenge, ChallengeAdmin)
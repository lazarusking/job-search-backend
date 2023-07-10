
# Register your models here.
from typing import Any, Iterator, List, Optional
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth import get_user_model

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest
from .models import User, Recruiter, Profile, RecruiterProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class RecruiterProfileInline(admin.StackedInline):
    model = RecruiterProfile
    can_delete = False
    verbose_name_plural = "profile"


# class CustomUserAdmin(admin.ModelAdmin):
#     # model = User
#     inlines = [ProfileInline]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'is_staff','is_recruiter']
    fieldsets = (
        (('Login'), {'fields': ('username', 'email', 'password')}),
        (('Personal Info'), {'fields': ('first_name',
         'last_name',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (('Important Dates'), {'fields': ('date_joined',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    inlines = [ProfileInline]
    recruiter_inline = [RecruiterProfileInline]

    # def get_formsets_with_inlines(self, request: HttpRequest, obj=None) -> Iterator[Any]:
    #     # super().get_formsets_with_inlines(request, obj)
    #     for inline in self.get_inline_instances(request, obj):
    #         print(isinstance(inline, ProfileInline), hasattr(obj, 'recruiter'))
    #         if hasattr(obj, 'recruiter'):
    #             if isinstance(inline, ProfileInline):
    #                 print(inline, obj, request.user)
    #                 yield inline.get_formset(request, obj), inline
    #         else:
    #             # if not isinstance(inline,ProfileInline):
    #             print(inline)
    #             yield inline.get_formset(request, obj), inline
    def get_inlines(self, request: HttpRequest, obj=None):
        print(obj)
        return (self.recruiter_inline if hasattr(obj, 'is_recruiter') and obj.is_recruiter else self.inlines)


class CustomRecruiterAdmin(CustomUserAdmin):
    # model = Recruiter
    # # list_display = ['email', 'username', 'is_staff', 'is_recruiter']
    # inlines = [RecruiterProfileInline]
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Recruiter)
admin.site.register(RecruiterProfile)

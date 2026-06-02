from .models import User, OtpCode, Avatar
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.safestring import mark_safe


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ['is_admin']
    readonly_fields = ('last_login',)

    fieldsets = [
        [None, {'fields':['email', 'phone_number', 'full_name', 'password']}],
        ['Permissions', {'fields': ['is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions']}]
    ]

    add_fieldsets = [
        [None, {'fields': ['phone_number', 'email', 'full_name', 'password1', 'password2']}]
    ]

    def get_form(self, request, obj = None,  **kwargs):
        form = super().get_form(request, obj , **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form #برای غیر فعال کردن فرم مورد نظر
    #مثلا یه کاربری میخواد تمام مجوز هارو داشته باشه ولی سوپریوز نباشه

    search_fields = ['email', 'full_name']
    ordering = ('full_name', )
    filter_horizontal = ['groups', 'user_permissions']

    def response_change(self, request, obj):
        if '_saveupper' in request.POST:
            obj.full_name = obj.full_name.upper()
            obj.save()
            self.message_user(request, 'object saved uppercase', 'success')
            return redirect('admin:accounts_user_changelist')
        return super().response_change(request, obj)#if user want button for save

admin.site.register(User, UserAdmin)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    readonly_fields = ['avatar_pic']
    
    def avatar_pic(self, obj):
        return mark_safe(f"<img src='{obj.picture.url}' width='{obj.picture.width}'/>")

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')
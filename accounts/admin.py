from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class UserResource(resources.ModelResource):
   class Meta:
      model = CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):

  resource_class = UserResource
  form = UserChangeForm
  add_form = UserCreationForm

  fieldsets = (
    (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    ('Permission', {'fields': ('is_active', 'is_admin', 'is_superuser', 'is_verified', 'groups', 'user_permissions')})
  )

  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',),
        }),
    )
  
  list_display = ('email', 'is_superuser')
  list_filter = ('email', 'is_active',)
  search_fields = ('email',)
  ordering = ('email',)
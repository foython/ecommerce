from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser



class UserCreationForm(forms.ModelForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password...'}), )
  password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter Password...'}))

  class Meta:
    model = CustomUser
    fields = ('first_name', 'last_name', 'email' )
    widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
               'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
               'email': forms.TextInput(attrs={'placeholder': 'Email'})              
               }
    

  def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

  def save(self, commit=True):
      # Save the provided password in hashed format
      user = super().save(commit=False)
      user.set_password(self.cleaned_data["password1"])
      if commit:
          user.save()
      return user

class UserChangeForm(forms.ModelForm):
  
  """A form for updating users. Includes all the fields on
  the user, but replaces the password field with admin's
  disabled password hash display field.
  """
  password = ReadOnlyPasswordHashField()

  class Meta:
    model = CustomUser
    fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_superuser')
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name', 'phone_number', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_number', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('phone_number','name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name','password1', 'password2')}
        ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()

# -------------------inline----------------------------------------
class CityInline(admin.StackedInline):
    show_change_link = True
    model = City

class HotelInline(admin.TabularInline):
    show_change_link = True
    model = Hotel

class HotelLogoInline(admin.TabularInline):
    model = HotelLogoImg

class HouseInline(admin.StackedInline):
    show_change_link = True
    model = House

class HousePackageInline(admin.StackedInline):
    show_change_link = True
    model = HousePackage
    extra = 0
    verbose_name = '套餐'
    verbose_name_plural = '套餐'
    fields = ('package_name','need_point','package_state','detail')

# -------------------inline-----end-----------------------------------

class ProvinceAdmin(ModelAdmin):
    list_display = ('id','name','name_py',)
    inlines = [CityInline,]


class CityAdmin(ModelAdmin):
    list_display = ('name_py', 'name','logo', 'province')
    inlines = [HotelInline,]

class InstallationAdmin(ModelAdmin):
    list_display = ('deviceToken',)




class HotelAdmin(ModelAdmin):
    inlines = [HotelLogoInline,HouseInline]

class HotelLogoImgAdmin(ModelAdmin):
    pass



class HouseAdmin(ModelAdmin):
    inlines = [HousePackageInline,]
    pass





# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Installation,InstallationAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(HotelLogoImg,HotelLogoImgAdmin)
admin.site.register(House,HouseAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



# Register your models here


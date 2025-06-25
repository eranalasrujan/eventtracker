from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Import UserChangeForm
from.models import CustomUser

# Form for editing existing user details (e.g., in admin or profile page)
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'batch'] # Exclude password for editing

# Form for new user registration
class UserRegistrationForm(UserCreationForm):
    # Add 'role' and 'batch' fields to the registration form
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, initial='student', widget=forms.Select(attrs={'class': 'form-control'})) # Default to student
    batch = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'})) # Optional batch field
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'})) # Make email required

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Explicitly list all desired fields for user creation, including your custom fields.
        # UserCreationForm handles the password fields automatically.
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'batch')

    # Override save to ensure role and batch are set correctly (UserCreationForm handles password hashing)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.batch = self.cleaned_data['batch']
        user.email = self.cleaned_data['email'] # Ensure email is saved
        if commit:
            user.save()
        return user

# Custom form for changing existing user details in admin (if needed, otherwise CustomUserForm is fine)
class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    batch = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        # Explicitly list all desired fields for changing an existing user, including your custom fields.
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role', 'batch')
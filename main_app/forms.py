from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'date_of_birth'] # add your additional fields here

class CustomUserCreationForm(UserCreationForm):
    profile = ProfileForm()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        profile_data = self.cleaned_data.get('profile')
        if profile_data:
            profile = Profile.objects.create(user=user, **profile_data)
            profile.save()
        return user
    


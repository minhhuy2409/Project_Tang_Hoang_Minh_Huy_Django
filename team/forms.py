from django import forms
from .models import Player, Attendance, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'shirt_number', 'position', 'foot', 'playing_style', 'health_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shirt_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'foot': forms.Select(attrs={'class': 'form-control'}),
            'playing_style': forms.Select(attrs={'class': 'form-control'}),
            'health_status': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Attendance.STATUS_CHOICES, attrs={'class': 'form-control'}),
        }

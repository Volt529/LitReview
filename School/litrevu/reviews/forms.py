from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    """Formulaire pour créer/modifier un ticket"""
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Titre du livre / article'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Décrivez ce que vous recherchez...',
                'rows': 4
            }),
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }


class ReviewForm(forms.ModelForm):
    """Formulaire pour créer/modifier une critique"""
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={
                'placeholder': 'Titre de la critique'
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Votre commentaire...',
                'rows': 5
            }),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(6)])
        }
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire',
        }


class TicketReviewForm(forms.Form):
    """Formulaire combiné pour créer un ticket ET une critique en même temps"""
    # Champs du ticket
    ticket_title = forms.CharField(
        max_length=128,
        label='Titre',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre du livre / article'
        })
    )
    ticket_description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.Textarea(attrs={
            'placeholder': 'Description (optionnelle)',
            'rows': 3
        })
    )
    ticket_image = forms.ImageField(
        required=False,
        label='Image'
    )
    
    # Champs de la critique
    review_headline = forms.CharField(
        max_length=128,
        label='Titre de la critique',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre de votre critique'
        })
    )
    review_rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        label='Note',
        widget=forms.RadioSelect(choices=[(i, i) for i in range(6)])
    )
    review_body = forms.CharField(
        required=False,
        label='Commentaire',
        widget=forms.Textarea(attrs={
            'placeholder': 'Votre commentaire (optionnel)',
            'rows': 5
        })
    )
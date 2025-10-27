from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    """Modèle pour une demande de critique"""
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    image = models.ImageField(upload_to='tickets/', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.title


class Review(models.Model):
    """Modèle pour une critique"""
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f"{self.headline} - {self.rating}/5"


class UserFollows(models.Model):
    """Modèle pour les abonnements entre utilisateurs"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
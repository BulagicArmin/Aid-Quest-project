from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User, Profile


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Naziv")
    content = models.TextField(verbose_name="Opis")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    uplatni_racun = models.CharField(max_length=55, blank=True)
    adresa = models.CharField(max_length=55, blank=True)
    stanje = models.BooleanField(default=True)
    hitnost = models.BooleanField(default=False)
    prikupljeno = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

    def povecaj(self, num):
        self.prikupljeno += num


class Zahtjev(models.Model):
    title = models.CharField(max_length=100, verbose_name="Naziv")
    content = models.TextField(verbose_name="Opis pomoci")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    potrebna_sr = models.CharField(max_length=100, verbose_name="Potrebna sredstva")
    hum_org = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('zahtjev-detail', kwargs={'pk':self.pk})




from django.db import models
from django.urls import reverse
from .validators import validate_video_format

# Create your models here.

class Ad(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.CharField(
        max_length=2,
        choices=[
            ('TA', 'Танки'),
            ('HE', 'Хилы'),
            ('DD', 'ДД'),
            ('TO', 'Торговцы'),
            ('GI', 'Гилдмастеры'),
            ('KV', 'Квестгиверы'),
            ('KU', 'Кузнецы'),
            ('KO', 'Кожевники'),
            ('ZE', 'Зельевары'),
            ('MZ', 'Мастера заклинаний')
        ],
        default='TA'
    )
    posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True,
                             validators=[validate_video_format])

    def __str__(self):
        return f'{self.title} ({self.posted.ctime()})'

    def get_absolute_url(self):
        return reverse('ad_detail', kwargs={'pk': self.pk})


class Offer(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        if len(self.text) < 50:
            snippet = self.text
        else:
            snippet = self.text[:50].rsplit(' ', 1)[0] + '...'

        return f'{snippet} ({self.posted.ctime()})'
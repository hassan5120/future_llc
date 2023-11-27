from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review_text = models.TextField()
    image = models.ImageField(default='', upload_to='',blank=True, null=True)
    field_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
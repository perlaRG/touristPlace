from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    
    email = models.EmailField(unique=True)
    
    contraseña = models.CharField(max_length=100)
    
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre
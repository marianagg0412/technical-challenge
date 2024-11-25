from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Set default role for superusers
        from .models import Role
        default_role, created = Role.objects.get_or_create(role="Admin")
        extra_fields.setdefault('role', default_role)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'


class Cycle(models.Model):
    semester = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"Semester {self.semester}, Year {self.year}"

class Control(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="controls")
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="controls", default=1)
    date_elaborated = models.DateField(blank=True, null=True)  # Fecha de elaboración
    status = models.CharField(max_length=50, default='Sin iniciar')  # Estado
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Total Horas Invertidas
    consulted_resources = models.TextField(blank=True, null=True)  # Recursos Consultados

    def __str__(self):
        return self.name



class Validation(models.Model):
    STATUS_CHOICES = [
        ('En proceso', 'En proceso'),
        ('Terminado', 'Terminado'),
        ('Sin iniciar', 'Sin iniciar'),
        ('No evaluado', 'No evaluado'),
    ]

    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name="validations")
    design_score = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date_elaborated = models.DateField(blank=True, null=True)  # Fecha de elaboración
    person_name = models.CharField(max_length=255, blank=True, null=True)  # Nombre de la persona
    person_role = models.CharField(max_length=255, blank=True, null=True)  # Cargo de la persona

    def save(self, *args, **kwargs):
        if self.design_score is None:
            self.status = 'No evaluado'
        elif self.design_score >= 80:
            self.status = 'Terminado'
        else:
            self.status = 'En proceso'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Validation of {self.control.name} - Status: {self.status}"


class DesignQuestion(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name="questions")
    is_required = models.BooleanField(default=True)
    question = models.TextField(default='')

    def __str__(self):
        return f"Question for {self.control.name} (Required: {self.is_required})"


class DesignAnswer(models.Model):
    YES_NO_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
        ('No Aplica', 'No Aplica'),
    ]

    question = models.ForeignKey(DesignQuestion, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=20, choices=YES_NO_CHOICES, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)  # Explanation field for the answer

    def __str__(self):
        return f"Answer to Question {self.question.id} for Validation"

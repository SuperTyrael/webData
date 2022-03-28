from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Professor(models.Model):
    id = models.CharField(
        primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Module(models.Model):
    code = models.CharField(primary_key=True, max_length=60)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ModuleInstance(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    professor = models.ManyToManyField(Professor)

    def __str__(self):
        return str(self.module) + ", " + str(self.year) + ", " + str(self.semester) + ", " + str(self.professor.all())


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.module)+" "+str(self.rate)

# class Responsible(models.Model):
#     professor_name = models.ForeignKey(Professor, on_delete=models.CASCADE)
#     module = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.responsible_name

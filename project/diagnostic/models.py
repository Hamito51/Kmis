from django.db import models


# Для работы с массивами создаем дополнительные классы и реализуем отношение ManyToMany 
class Device(models.Model):
	device_name = models.CharField(max_length=120)
	device_id = models.IntegerField()


class Results(models.Model):
	heart_rate = models.IntegerField()
	bp_syst = models.IntegerField()
	bp_diast = models.IntegerField()


class Diagnostic(models.Model):
	name = models.CharField(max_length=120)
	date = models.CharField(max_length=25)
	device = models.ManyToManyField(Device)
	description = models.TextField()
	conclusion = models.TextField()
	file = models.TextField()
	file_md5 = models.TextField()
	results = models.ManyToManyField(Results)


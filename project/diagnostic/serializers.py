from datetime import datetime
from rest_framework import serializers
from .models import Diagnostic, Device, Results


# Создаем Сериализаторы на основе наших моделей.
class DeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Device
		fields = ('device_name', 'device_id')


class ResultsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Results
		fields = ('heart_rate', 'bp_syst', 'bp_diast')


class DiagnosticSerializer(serializers.ModelSerializer):
	device = DeviceSerializer(many=True)
	results = ResultsSerializer(many=True)

	class Meta:
		model = Diagnostic
		fields = ['name', 'date', 'device', 'description', 'conclusion', 'file', 'file_md5', 'results'] 

	def create(self, validated_data):
		# Приводим поля к необходимому формату
		name = validated_data.get('name').split(' (')[0]
		date = validated_data.get("date").split('T')[0]
		date = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')

		description = validated_data.get("description")
		conclusion = validated_data.get("conclusion")
		file = validated_data.get("file")
		file_md5 = validated_data.get("file_md5")
		# Получаем данные из массивов.
		device_name = (validated_data.get("device")[0]).get('device_name')
		device_id = (validated_data.get("device")[0]).get('device_id')
		heart_rate = (validated_data.get("results")[0]).get('heart_rate')
		bp_syst = (validated_data.get("results")[0]).get('bp_syst')
		bp_diast = (validated_data.get("results")[0]).get('bp_diast')
		# Создаем экземпляр класса
		instance = Diagnostic.objects.create(name=name, 
										  date=date, 
										  description=description, 
										  conclusion=conclusion, 
										  file=file, 
										  file_md5=file_md5)
		# Создаем массивы и добавляем их в экземпляр
		device_instance = Device.objects.create(device_name=device_name, 
												device_id=device_id)
		results_instance = Results.objects.create(heart_rate=heart_rate, 
												  bp_syst=bp_syst, 
												  bp_diast=bp_diast)
		instance.device.add(device_instance)
		instance.results.add(results_instance)
		return instance
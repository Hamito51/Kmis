import os
from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from project.settings import STATIC_ROOT
from rest_framework.views import APIView
from .models import Diagnostic, Device, Results
from .serializers import DiagnosticSerializer
from .script import *


# Подтягиваем в переменные тестовые документы
xml_file = os.path.join(STATIC_ROOT, "Document.XML")
JSON_File = os.path.join(STATIC_ROOT, "devices.json")
image_file = os.path.join(STATIC_ROOT, "instrumental_diagnostic.png")


# Функция получает данные из представленных файлов и сохраняит их в JSON
def get_from_files():
	parser_dict = (get_dict(xml_file, JSON_File, image_file))
	# Приводим поля к необходимому формату
	name = parser_dict["name"].split(' (')[0]
	date = datetime.strptime(parser_dict["date"].split('T')[0], '%d.%m.%Y').strftime('%Y-%m-%d')
	# Создаем экземпляр класса
	instance = Diagnostic.objects.create(name=name,
	  							 		 date=date,
	 							 		 description=parser_dict["description"],
	 							 		 conclusion=parser_dict["conclusion"],
	 							 		 file=parser_dict["file"],
	 							 		 file_md5=parser_dict["file_md5"]
	  )
	# Создаем массивы и добавляем их в экземпляр
	device_instance = Device.objects.create(device_name=parser_dict["device"], 
											device_id=parser_dict["device_id"])
	device_instance.save()
	results_instance = Results.objects.create(heart_rate=parser_dict["heart_rate"], 
										 	  bp_syst=parser_dict["bp_syst"], 
										 	  bp_diast=parser_dict["bp_diast"])
	results_instance.save()
	instance.device.add(device_instance)
	instance.results.add(results_instance)
	instance.save() 
	return instance


# Создаем класс для отображения списка списка принятых пакетов данных инструментальная диагностика
class DiagnosticView(APIView):
	# Отображение списка
	def get(self, request):
		diagnostics = Diagnostic.objects.all()
		serializer = DiagnosticSerializer(diagnostics, many=True)
		return Response({"diagnostic": serializer.data})
	# Отправка пакета
	def post(self, request):
		# Получаем параметр из Query Params для определения будем ли использовать тестовые файлы
		key = (request.query_params.get('key'))
		# Если, полученный параметр удовлетворяет условию, то вызываем парсер из скрипта и получаем данные
		if key == 'yes':
			instance = get_from_files()
			return Response({"success": "Diagnostic for '{}' created successfully".format(instance.name)})
		else:
			# При любом другом значении параметра получаем данные, отправленные через запрос
			diagnostic = request.data.get('diagnostic')
			serializer = DiagnosticSerializer(data=diagnostic)
			if serializer.is_valid(raise_exception=True):
				diagnostic_saved = serializer.save()
			return Response({"success": "Diagnostic for '{}' created successfully".format(diagnostic_saved.name)})

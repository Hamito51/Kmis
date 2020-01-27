from lxml import etree, objectify
import json
import base64
import hashlib
 

# Получаем данные из файла Document.xml
def parseXML(xmlFile):
    with open(xmlFile, 'rb') as f:
        xml = f.read()
    root = objectify.fromstring(xml)
    # Поля, из которых нам нужны данные
    fields = ['name','date', 'device', 'description', 'conclusion', 'bp_syst', 'bp_diast', 'heart_rate']
    # Словарь, в котором будем хранить полученные данные
    parser_dict = {}
    # Получаем атрибуты первого поколения
    for tag_1 in root.getchildren():
        attrib_1 = tag_1.attrib
    # Получаем атрибуты второго поколения    
        for tag_2 in tag_1.getchildren():
            attrib_2 = tag_2.attrib
    # Если поле в нашем списке, добавляем пару в наш словарь        
            if attrib_1.get("name") in fields:
                parser_dict[attrib_1.get('name')] = tag_2.text
    # Получаем атрибуты третьего поколения             
            for tag_3 in tag_2.getchildren():
               pass
    # Если поле в нашем списке, добавляем пару в наш словарь           
            if attrib_2.get("name") in fields:
                 parser_dict[attrib_2.get('name')] = tag_3.text  
    return parser_dict

# Получаем данные из файла devices.json
def get_device_id(JSON_File, device_name):
    with open(JSON_File, "r") as read_file:
        data = json.load(read_file)
    # Ищем в файле название оборудования, которое мы получили в результате парсинга
    for device in data:
        # Проверяем, чтобы оборудование удовлетворяло нашим требованиям и возвращаем идентификационный номер
        if (device["name"] == device_name) and device["available"] and not device["is_active"]:
            return(device["id"])

# Преобразуем файл изображения в base64 и получаем md5
def make_b64_md5(image_file):
    with open(image_file, "rb") as image_file:
        image = image_file.read()
    encoded_string = base64.b64encode(image)
    md5 = hashlib.md5(image).hexdigest()
    return encoded_string, md5

# Функция для вызова вспомогательных функций
def get_dict(xml_file, JSON_File, image_file):
    parser_dict = parseXML(xml_file)
    # Записываем в переменную название оборудования, полученного в результате парсинга
    device_name = parser_dict['device']
    parser_dict["device_id"] = get_device_id(JSON_File, device_name)
    parser_dict["file"], parser_dict["file_md5"] = make_b64_md5(image_file)
    return parser_dict

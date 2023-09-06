import json
import yaml


def addFieldInJson(value, field, data):
    type_ = type(value)
    
    if type_ == str :
        if(len(value) == 0): 
            value = "string"
        data[field] = {
                    'type': 'string',
                    'description': '',
                    'example' : value
        }
    elif type_ == int or type_ == float:
        data[field] = {
                    'type': 'number',
                    'description': '',
                    'example' : value
        }
    elif type_ == bool: 
        data[field] = {
                    'type': 'boolean',
                    'description': '',
                    'example' : value
        }
    elif type_ == dict: 
        json2 = value
        data2 = {}
        for key in json2.keys():
            addFieldInJson(json2[key], key, data2)

        data[field] = {
            'type': "object",
            'properties': data2
        }
    elif type_ == list:
        list_ = value
        listItem = list_[0]
        data2 = {}

        addFieldInJson(listItem, field, data2)
        data[field] = {
            'type': 'array',
            'items': data2[field]
        }
    else:
         data[field] = {
                    'type': 'string',
                    'description': '',
        }
    

json_path = input("Passe o path do arquivo json: ")
outsource = 'component.yaml'
json_data = None

with open(json_path, 'r') as archive:
    json_data = json.load(archive)

data = {}
for key in json_data.keys():

    if type(json_data[key]) == dict: 
        data2 = {}
        json = json_data[key]
        for key2 in json.keys():
            addFieldInJson(json[key2], key2, data2)
       
        data[key] = {
            'type': 'object',
            'properties': data2
        }
    elif type(json_data[key]) == list:
        list_ = json_data[key]
        listItem = list_[0]
        data2 = {}

        addFieldInJson(listItem, key, data2)
        data[key] = {
            'type': 'array',
            'items': data2[key]
        }
    else:
        addFieldInJson(json_data[key], key, data)

with open(outsource, 'w') as archive:
    yaml.dump(data, archive, sort_keys=False)

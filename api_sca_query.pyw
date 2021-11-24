from pyodbc import connect
from json import dump
from datetime import datetime
from time import sleep

time_request = []
time_request_hd = []
time_request_list = 0
delay_min = 0


def generator_json():
    lines = []
    t3 = []
    t1 = []
    t2 = []
    area_key = ''
    floor_json = {'datetime': 0, 't3': {'16': {'a': 0, 'b': 0}, '15': {'a': 0, 'b': 0}, '14': {'a': 0, 'b': 0},
                                        '13': {'a': 0, 'b': 0}, '12': {'a': 0, 'b': 0}, '11': {'a': 0, 'b': 0},
                                        '10': {'a': 0, 'b': 0}, '9': {'a': 0, 'b': 0}, '8': {'a': 0, 'b': 0},
                                        '7': {'a': 0, 'b': 0}, '6': {'a': 0, 'b': 0}, '5': {'a': 0, 'b': 0},
                                        '4': {'a': 0, 'b': 0}, '3': {'a': 0, 'b': 0}, '2': {'a': 0, 'b': 0},
                                        '1': {'a': 0, 'b': 0}, '0': {'a': 0, 'b': 0}},
                                 't1': {'16': {'a': 0, 'b': 0}, '15': {'a': 0, 'b': 0}, '14': {'a': 0, 'b': 0},
                                        '13': {'a': 0, 'b': 0}, '12': {'a': 0, 'b': 0}, '11': {'a': 0, 'b': 0},
                                        '10': {'a': 0, 'b': 0}, '9': {'a': 0, 'b': 0}, '8': {'a': 0, 'b': 0},
                                        '7': {'a': 0, 'b': 0}, '6': {'a': 0, 'b': 0}, '5': {'a': 0, 'b': 0},
                                        '4': {'a': 0, 'b': 0}, '3': {'a': 0, 'b': 0}, '2': {'a': 0, 'b': 0},
                                        '1': {'a': 0, 'b': 0}, '0': {'a': 0, 'b': 0}},
                                 't2': {'16': {'a': 0, 'b': 0}, '15': {'a': 0, 'b': 0}, '14': {'a': 0, 'b': 0},
                                        '13': {'a': 0, 'b': 0}, '12': {'a': 0, 'b': 0}, '11': {'a': 0, 'b': 0},
                                        '10': {'a': 0, 'b': 0}, '9': {'a': 0, 'b': 0}, '8': {'a': 0, 'b': 0},
                                        '7': {'a': 0, 'b': 0}, '6': {'a': 0, 'b': 0}, '5': {'a': 0, 'b': 0},
                                        '4': {'a': 0, 'b': 0}, '3': {'a': 0, 'b': 0}, '2': {'a': 0, 'b': 0},
                                        '1': {'a': 0, 'b': 0}, '0': {'a': 0, 'b': 0}}}

    config_json = open('config', 'r').readline().split(';')
    data_connect = ("DRIVER={" + f"{config_json[3]}" + "};" + f"SERVER={config_json[0]};UID={config_json[1]};"
                                                              f"PWD={config_json[2]}")
    connect_db = connect(data_connect)
    cursor = connect_db.cursor()
    cursor.execute("SET NOCOUNT ON;" + (open("numberPeopleOnFloor.sql").read()))
    rows = cursor.fetchall()
    cursor.close()

    for row in rows:
        lines.append(row)

    for line in lines:
        if line[1] == 'AC':
            t3.append(line)
        elif line[1] == 'T1':
            t1.append(line)
        elif line[1] == 'T2':
            t2.append(line)

    areas = {'t3': {'t3': t3}, 't1': {'t1': t1}, 't2': {'t2': t2}}

    for area in areas.values():
        if 't3' in area.keys():
            area_key = 't3'
        elif 't1' in area.keys():
            area_key = 't1'
        elif 't2' in area.keys():
            area_key = 't2'
        for companys in area.values():
            for company in companys:
                for a in range(0, 16):
                    if company[0] not in ['Selecionar...', '', 'Externo']:
                        if company[0] != '':
                            if company[3] == 'THB' and company[0] == '09' and int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['a'] += company[2]
                            elif company[3] == 'Mills' and company[0] == '04' and int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['a'] += company[2]
                            elif company[3] == 'GAP7' and company[0] == '04' and int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['b'] += company[2]
                            elif company[3] == 'Innova' and company[0] == '00' and int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['b'] += company[2]
                            elif company[3] == 'Hagana' and company[0] == '00' and int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['a'] += company[2]
                            elif int(company[0]) == a:
                                floor_json[f'{area_key}'][f'{int(company[0])}']['a'] += company[2]
                                floor_json[f'{area_key}'][f'{int (company[0])}']['b'] = 0
                    else:
                        floor_json[f'{area_key}']['16']['a'] += company[2]
                        floor_json[f'{area_key}']['16']['b'] += 0
                        break
    floor_json['datetime'] = str(datetime.now())
    dump(floor_json, open('floor.json', 'w', encoding = 'utf-8'), ensure_ascii = False, indent = 4)
    return config_json, floor_json


while time_request_list < 59:
    time_request_list += 1
    time_request.append(time_request_list)
time_request = list(filter(lambda time: time < 60, time_request))

while True:
    if datetime.now().minute in time_request and delay_min != datetime.now().minute:
        delay_min = datetime.now().minute
        config, floor = generator_json()
    sleep(1)

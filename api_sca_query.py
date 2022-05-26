from pyodbc import connect
from json import dump
from datetime import datetime
from time import sleep
from os import system

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
    floor = {'datetime': 0,
             't3': {'16': 0, '15': 0, '14': 0, '13': 0, '12': 0, '11': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0,
                    '5': 0, '4': 0, '3': 0, '2': 0, '1': 0, '0': 0},
             't1': {'16': 0, '15': 0, '14': 0, '13': 0, '12': 0, '11': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0,
                    '5': 0, '4': 0, '3': 0, '2': 0, '1': 0, '0': 0},
             't2': {'16': 0, '15': 0, '14': 0, '13': 0, '12': 0, '11': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0,
                    '5': 0, '4': 0, '3': 0, '2': 0, '1': 0, '0': 0}}

    config = open('config', 'r').readline().split(';')
    data_connect = ("DRIVER={" + f"{config[3]}" + "};" + f"SERVER={config[0]};UID={config[1]};PWD={config[2]}")
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
                    if company[0] not in ['Selecionar...', '']:
                        if company[0] != '':
                            if int(company[0]) == a:
                                floor[f'{area_key}'][f'{int(company[0])}'] += company[2]
                    else:
                        floor[f'{area_key}']['16'] += company[2]
                        break

    floor['datetime'] = str(datetime.now())
    dump(floor, open('floor.json', 'w', encoding = 'utf-8'), ensure_ascii = False, indent = 4)
    return config, floor


while time_request_list < 59:
    time_request_list += 1
    time_request.append(time_request_list)
time_request = list(filter(lambda time: time < 60, time_request))

while True:
    if datetime.now().minute in time_request and delay_min != datetime.now().minute:
        delay_min = datetime.now().minute
        config, floor = generator_json()
        system("cls")
        print(f"""
              -----------------Database connection----------------
              Driver: {config[3]}
              Server: {config[0]}
              User SQL: {config[1]}
              Passsword: {config[2]}
              --------------------Defined Network-----------------
              IP: localhost
              Door: 1010
              Time Request: Every 1 minutes.
              Data-Time-Now: {datetime.now ()}
            ------------------------------------------------------
Generad JSON: {floor}
              """)
    sleep(1)

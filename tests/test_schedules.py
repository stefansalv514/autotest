import btoken
import requests
import json
import db

headers = btoken.get_token()
ip="http://192.168.77.116"
start = db.startdb
stop = db.stopdb

# БД
table = "schedules"


# Старт подключения к БД по SSH
def test_startserver():
    global conn, server
    conn, server = start()
#
#
# # # # 1)Положительное тестирование, Добавление нового графика работы +++++Косяк не мой+++++
# def test_schedules_add():
#     url = ip + '/schedules/add'
#
#     acronimsdata = "zazu"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() != None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"] == "Успешно создано", "Неверное содержание message"
#     assert response.status_code == 201, "Неверный код ответа"
# #
# #
# #
# # # 2)Добавление Добавление нового графика работы с превышением допустимого кол-ва знаков +++++
# def test_schedules_add_max_limit_values():
#     url = ip + '/schedules/add'
#
#     acronimsdata = "zazshthigstbjgishuitrsbjgsofjdapogiutiytuihjgsipbfgidshivfiagtuiibjyhriujhgtrhjyuirnhgjisnibgsihtuirhyuisbgisu"
#     weekdays_data = 34354236546547365354265423542365473653763765365245614356467578659848653754632654736548746542635736487658647644
#     weekends_data = 34354236546547365354265423542365473653763765365245614356467578659848653754632654736548746542635736487658647644
#     float_data = 0
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "float": float_data
#             }
#
#     # Вызов функции подготовки БД для выполнения теста
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == 'Значение acronim должно быть меньше или равно 30 символам.', \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekdays"][0] == 'Значение weekdays должно иметь корректное целочисленное значение.',\
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends должно иметь корректное целочисленное значение.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 3)Добавление проекта с некорректным типом данных +++++
# def test_schedules_add_error_type_values():
#     url = ip + '/schedules/add'
#
#     acronimsdata = 128
#     weekdays_data = "3"
#     weekends_data = "7"
#     descriptionsdata = "description"
#     float_data = "5"
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#             }
#
#     # Вызов функции подготовки БД для выполнения теста
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть корректным строковым значением.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekdays"][0] == "Значение weekdays должно быть корректным целочисленным значением.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends должно быть корректным целочисленным значением.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["float"][0] == "Значение float должно быть корректным булевым значением.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 4)Тест на уникальность поля acronim +++++
# def test_schedules_add_unique_acronim():
#     url = ip + '/schedules/add'
#
#     acronimsdata = "zazu"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     acronimsdata_sec = "zazu"
#     weekdays_data_sec = 3
#     weekends_data_sec = 2
#     descriptionsdata_sec = "description"
#     float_data_sec = False
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#             }
#
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata_sec, weekdays_data_sec, weekends_data_sec, descriptionsdata_sec, float_data_sec,))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть уникальным.", "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 5)тест на значения None в ключах запроса +++++
# def test_schedules_add_none_values():
#     url = ip + '/schedules/add'
#
#     acronimsdata = None
#     weekdays_data = None
#     weekends_data = None
#     descriptionsdata = None
#     float_data = None
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#             }
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekdays"][0] == "Значение weekdays является обязательным.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends является обязательным.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 6)тест на пустой запрос +++++
# def test_schedules_add_null_request():
#     url = ip + '/schedules/add'
#
#     body = {
#
#            }
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekdays"][0] == "Значение weekdays является обязательным.", \
#             "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends является обязательным.", \
#             "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 1)Получение графиков по акрониму +++++Косяк не мой+++++
# def test_schedules_get():
#     url = ip + '/schedules/get'
#
#     acronimsdata = "zazu"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     body = {
#         "acronims": [acronimsdata]
#     }
#
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata, weekdays_data, weekends_data, descriptionsdata, float_data))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#     print(requestdict)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == acronimsdata, "Неверное содержание message"
#     assert response.status_code == 200, "Неверный код ответа"
#
#
# # 2)Получение графиков по акрониму ---Косяк не мой---
# # Тест на запрос с 2 истинными и 1 ложным ключом
# def test_schedules_get_correct_and_incorrect_key():
#     url = ip + '/schedules/get'
#
#     acronimsdata = "zazu"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     acronimsdata_sec = "venom"
#     weekdays_data_sec = 3
#     weekends_data_sec = 2
#     descriptionsdata_sec = "description"
#     float_data_sec = False
#
#     acronims_data_tr = "super"
#
#     body = {
#         "acronims": [acronimsdata]
#            }
#
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata, weekdays_data, weekends_data, descriptionsdata, float_data))
#         conn.commit()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata_sec, weekdays_data_sec, weekends_data_sec, descriptionsdata_sec, float_data_sec))
#         conn.commit()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronims_data_tr,))
#     if cur.fetchone() != None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronims_data_tr,))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims"][0] == acronimsdata, "Неверное содержание message"
#     assert requestdict["status"]["message"]["acronims"][0] == acronimsdata, "Неверное содержание message"
#     assert requestdict["status"]["message"]["acronims"][2] == "Выбранное значение acronims.2 является неверным.", \
#         "Неверное содержание message"
#     assert response.status_code == 200, "Неверный код ответа"
#
#
#
# # 3)Получение графиков по акрониму +++++
# # Тест на превышение максимального количества знаков в значениях ключей
# def test_schedules_get_max_limit_values():
#     url = ip + '/schedules/get'
#
#     acronimsdata = "zazshthigstbjgishuitrsbjgsofjdapogiutiytuihjgsipbfgidshivfiagtuiibjyhriujhgtrhjyuirnhgjisnibgsihtuirhyuisbgisu"
#
#     body = {
#         "acronims": [acronimsdata]
#            }
#
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == 'Выбранное значение acronims.0 является неверным.', \
#             "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 5)Получение графиков по акрониму +++++
# # Пустой запрос
# def test_schedules_get_null_request():
#     url = ip + '/schedules/get'
#
#     body = {
#
#            }
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     cur = conn.cursor()
#     cur.execute("SELECT COUNT(*) FROM projects")
#     assert (cur.fetchone()) != (len(requestdict["data"]),)
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 6)Получение графиков по акрониму +++++++Косяк с кодом (не мой)+++++
# # None (null)
# def test_schedules_get_none_values():
#     url = ip + '/schedules/get'
#
#     acronimsdata = None
#
#     body = {
#         "acronim": [acronimsdata]
#            }
#
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims.0 должно быть корректным строковым значением.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 7)Получение графиков по акрониму +++++
# #Тест на запрос без массива
# def test_schedules_get_without_array():
#     url = ip + '/schedules/get'
#
#     acronimsdata = "venom"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     body = {
#         "acronims": acronimsdata
#            }
#
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#             (acronimsdata, weekdays_data, weekends_data, descriptionsdata, float_data))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims должно быть массивом.", \
#                 "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 8)Получение всех проектов (без параметров) или получение проектов по определенным параметрам +++++
# # Тест на запрос с 2 ложными ключами
# def test_schedules_get_incorrect_key():
#     url = ip + '/schedules/get'
#
#     acronimsdata = "zazu"
#     acronimsdata_sec = "venom"
#
#     body = {
#         "acronims": [acronimsdata, acronimsdata_sec]
#     }
#
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() != None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#         conn.commit()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#     if cur.fetchone() != None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#         conn.commit()
#
#     response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["acronims.1"][0] == "Выбранное значение acronims.1 является неверным.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
#Остановился здесь
# # 1)Обновление графика работы +++++Метод PUT не работает, работает только с POST+++++
# def test_schedules_update():
#     url = ip + '/schedules/update'
#
#     acronimsdata = "venom"
#     weekdays_data = 3
#     weekends_data = 2
#     descriptionsdata = "description"
#     float_data = False
#
#     acronimsdata_before = "venom"
#     weekdays_data_before = 1
#     weekends_data_before = 1
#     descriptionsdata_before = "qwerty"
#     float_data_before = False
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata
#            }
#
#     # Подготовка БД для выполнения теста
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata, weekdays_data, weekends_data, descriptionsdata, float_data))
#         conn.commit()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_before,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#             (acronimsdata_before, weekdays_data_before, weekends_data_before, descriptionsdata_before, float_data_before))
#         conn.commit()
#
#     # Запрос на обновление показателя
#     response = requests.put(url, json=body, headers=headers)
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверка БД на наличие обновленного показателя
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     assert cur.fetchone() != None, "В БД строка НЕ изменилась!"
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
#     assert response.status_code == 200, "Неверный код ответа"
#
#
# # 2)Обновление графика работы (пустое обновление) +++++
# def test_schedules_update_null_request():
#     url = ip + '/schedules/update'
#
#     body = {
#
#            }
#
#     # Запрос на обновление показателя
#     response = requests.put(url, json=body, headers=headers)
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
#     assert requestdict["status"]["message"]["description"][0] == "Значение description должно присутствовать и иметь непустое значение, если все из weekdays / weekends / description отсутствуют.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 3)Обновление графика работы (None) +++++
# def test_schedules_update_none_values():
#     url = ip + '/schedules/update'
#
#     acronimsdata = "venom"
#     weekdays_data = None
#     weekends_data = None
#     descriptionsdata = None
#     float_data = False
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#            }
#
#     # Запрос на обновление показателя
#     response = requests.put(url, json=body, headers=headers)
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["description"][0] == "Значение description должно присутствовать и иметь непустое значение, если все из weekdays / weekends / description отсутствуют.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # 4)Обновление графика работы +++++
# # Тест на превышение максимального количества знаков в значениях ключей
# def test_schedules_update_max_limit_values():
#     url = ip + '/schedules/update'
#
#     acronimsdata = "venom"
#     weekdays_data = 3215423654675436537524431542315432654736548675454673531241657654866345254326537698707865744324656686756765
#     weekends_data = 3254465789876543234556876543212345679876543214875654236464568746323456758432134567543245675432445675743275
#     descriptionsdata = "nysjhdjytdjhfgjytdkfgorogmklnbtorbkvlmnbonjhtnbgmnhjnlbmgjhnyonmklngoangmfkl;nhtosbmgklfnhtosbmgfshtn"
#     float_data = 4315432654276537542643251454365473648765874637534534311254765487564568767546354765486575463246546754736576538
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#             }
#
#     # Подготовка БД для выполнения теста
#     cur = conn.cursor()
#     cur.execute("SELECT FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     conn.commit()
#
#     # Запрос на обновление показателя
#     response = requests.put(url, json=body, headers=headers)
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверка БД на наличие обновленного показателя
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["weekdays"][0] == 'Значение weekdays должно иметь корректное целочисленное значение.', \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends должно иметь корректное целочисленное значение.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 5)Обновление графика работы -----Косяк не мой-----
# # # Тест на запрос с некорректными типами передаваемых данных в значениях ключей
# def test_schedules_update_incorrect_key():
#     url = ip + '/schedules/update'
#
#     acronimsdata = "venom"
#     weekdays_data = "3"
#     weekends_data = "2"
#     descriptionsdata = "desc"
#     float_data = "False"
#
#     acronimsdata_sec = "zazu"
#     weekdays_data_sec = 3
#     weekends_data_sec = 2
#     descriptionsdata_sec = "desc"
#     float_data_sec = False
#
#     body = {
#         "acronim": acronimsdata,
#         "weekdays": weekdays_data,
#         "weekends": weekends_data,
#         "description": descriptionsdata,
#         "float": float_data
#             }
#
#     # Подготовка БД для выполнения теста
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
#                     (acronimsdata_sec, weekdays_data_sec, weekends_data_sec, descriptionsdata_sec, float_data_sec))
#         conn.commit()
#
#     # Запрос на обновление показателя
#     response = requests.put(url, json=body, headers=headers)
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверка БД на наличие обновленного показателя
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["weekdays"][0] == "Значение weekdays должно быть корректным целочисленным значением.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["weekends"][0] == "Значение weekends должно быть корректным целочисленным значением.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["float"][0] == "Значение float должно быть корректным булевым значением.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 1)Отключение графика расписания (положительное тестирование) +++++
def test_schedules_delete():
    url = ip + '/schedules/delete'

    acronimsdata = "venom"
    weekdays_data = 3
    weekends_data = 2
    descriptionsdata = "desc"
    float_data = False

    acronimsdata_sec = "zazu"
    weekdays_data_sec = 3
    weekends_data_sec = 2
    descriptionsdata_sec = "desc"
    float_data_sec = False

    body = {
        "acronims": [acronimsdata, acronimsdata_sec]
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
            (acronimsdata_sec, weekdays_data_sec, weekends_data_sec, descriptionsdata_sec, float_data_sec))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, weekdays, weekends, description, float) VALUES (%s, %s, %s, %s, %s)",
            (acronimsdata, weekdays_data, weekends_data, descriptionsdata, float_data))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    assert cur.fetchone() == None, "В БД проект НЕ добавлен!"


    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"
#
#
# # 2)Удаление проектов по акрониму (пустое удаление) +++++
# def test_projects_delete_null_request():
#     url = ip + '/projects/delete'
#
#     body = {
#
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims является обязательным.", "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 3)Удаление проектов по акрониму (None) +++++
# def test_projects_delete_none():
#     url = ip + '/projects/delete'
#
#     acronimsdata = None
#
#     body = {
#         "acronims": [acronimsdata]
#             }
#
#     # Вызов функции подготовки БД для выполнения теста
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == "Значение acronims.0 должно быть корректным строковым значением.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 4)Удаление проектов по несуществующему акрониму +++++
# def test_projects_delete_incorrect_key():
#     url = ip + '/projects/delete'
#
#     acronimsdata = "super"
#
#     body = {
#         "acronims": [acronimsdata]
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#         conn.commit()
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.",\
#                                                                 "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 5)Удаление проектов по акрониму (положительное тестирование) +++++
# # #  Тест на указание 1 ложного и 1 истинного значений ключа
# def test_projects_delete_correct_and_incorrect_key():
#     url = ip + '/projects/delete'
#
#     acronimsdata = "pumba"
#     namesdata = "katrin"
#
#     acronimsdata_sec = "timon"
#
#     body = {
#         "acronims": [acronimsdata, acronimsdata_sec]
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s OR name = %s", (acronimsdata, namesdata))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
#         conn.commit()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#     if cur.fetchone() != None:
#         cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
#         conn.commit()
#
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     requestdict = json.loads(response.content)
#
#     # Проверка БД на наличие добавленного проекта
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND acronim = %s", (acronimsdata, acronimsdata_sec))
#     assert requestdict["status"]["message"]["acronims.1"][0] == "Выбранное значение acronims.1 является неверным.", \
#                                                                        "Неверное содержание message"
#     assert cur.fetchone() == None, "В БД проект НЕ добавлен!"
#
#
# # # 6)Удаление проектов по акрониму (положительное тестирование) +++++
# # # Тест на запрос без массива
# def test_projects_delete_without_array():
#     url = ip + '/projects/delete'
#
#     acronimsdata = "pumba"
#     namesdata = "katrin"
#
#     body = {
#         "acronims": acronimsdata
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#     if cur.fetchone() == None:
#         cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
#         conn.commit()
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверка БД на наличие добавленного проекта
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
#     assert cur.fetchone() != None, "В БД проект НЕ добавлен!"
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims должно быть массивом.", "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 8)Удаление проектов по акрониму (положительное тестирование) +++++
# # #  Тест на запрос с некорректными типами передаваемых данных в значениях ключей
# def test_projects_delete_error_type_values():
#     url = ip + '/projects/delete'
#
#     acronimsdata = 128
#
#     body = {
#         "acronims": [acronimsdata]
#     }
#
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == "Значение acronims.0 должно быть корректным строковым значением.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
# # # 9)Удаление проектов по акрониму (положительное тестирование) +++++
# # # Тест на превышение максимального количества знаков в значениях ключей
# def test_projects_delete_max_limit_values():
#     url = ip + '/projects/delete'
#
#     acronimsdata = "pumgjonhotjrsohbjgofjshtiojsrhyjrosbjhgorjshsrthobrgtjsojhytiosrjhiogjsoirgjtiosjhyiojshugjshuojtruiosjhtuiosrjba"
#
#     body = {
#         "acronims": [acronimsdata]
#            }
#
#     # Вызов функции подготовки БД для выполнения теста
#     cur = conn.cursor()
#
#     cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
#
#     response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
#     assert response.status_code != 500, "Ошибка от laravel"
#     assert response.status_code != 405, "Ошибка метода отправки"
#     requestdict = json.loads(response.content)
#
#     # Проверки на содержание message и верный статус код
#     assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.", \
#         "Неверное содержание message"
#     assert requestdict["status"]["message"]["acronims.0"][1] == "Значение acronims.0 должно быть меньше или равно 30 символам.", \
#         "Неверное содержание message"
#     assert response.status_code == 400, "Неверный код ответа"
#
#
#
#
# # Закрытие подключения к БД по SSH
def test_stopserver():
    stop(conn, server)


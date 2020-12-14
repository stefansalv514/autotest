import btoken
import requests
import json
import db

headers = btoken.get_token()
ip="http://192.168.77.116"
start = db.startdb
stop = db.stopdb

# БД
table = "projects"


# Старт подключения к БД по SSH
def test_startserver():
    global conn, server
    conn, server = start()
# #
# #
# # # 1)Положительное тестирование, добавление проекта +++++Косяк с кодом (не мой)+++++
def test_projects_add():
    url = ip + '/projects/add'

    acronimsdata = "test_acronim"
    namesdata = "test_name"
    descriptionsdata = "test_description"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s OR name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s OR name = %s", (acronimsdata, namesdata,))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() != None, "В БД добавлен проект не добавлен"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно создано", "Неверное содержание message"
    assert response.status_code == 201, "Неверный код ответа"
#
#
#
# # 2)Добавление проекта с превышением допустимого кол-ва знаков +++++
def test_projects_add_max_limit_values():
    url = ip + '/projects/add'

    acronimsdata = "zazуккпреыорпеоыгорипареырзоепщкшызропеыегрокпгшщызошпщзаоргокызроегзкыпзаыргезоргныорпазывпегu"
    namesdata = "hoатыпшгеыршрпшытпгешзуырфпавтмавфзтпкегшргшнтавыпегогрроыпшзмтаозвыштпгшзыетрзыкешрзшыкертзыкеmer"
    descriptionsdata = "qwertтмоаgohriotjrpogfodhsgtpuioghvfjdshgtihevihsfuiodhguiotrehvosfhduioghtuioevhuiosfdhgtuiorhe \n " \
                       "vuiofhdsuioghtuioevhfuidshguithrevuihfdsuighstieторгкншузтрнгшктриапоывтмзвфтргзктршзртиыкпотипаолдытиаз \n" \
                       "фптегзтрнзкгшытипаошытимаy"
    etl_project_idsdata = "1478165782431657824656556478356921675496543659263759745647836578241657796478356478564781"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "etl_project_id": etl_project_idsdata
           }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() == None, "В БД добавлен проект с превышением допустимого кол-ва знаков"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == 'Значение acronim должно быть меньше или равно 40 символам.', "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == 'Значение name должно быть меньше или равно 80 символам.', "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == 'Значение description должно быть меньше или равно 100 символам.', "Неверное содержание message"
    assert requestdict["status"]["message"]["etl_project_id"][0] == "Значение etl project id должно быть меньше или равно 40 символам.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 3)Добавление проекта с некорректным типом данных +++++
def test_projects_add_error_type_values():
    url = ip + '/projects/add'

    acronimsdata = "test_acronim"
    namesdata = "test_name"
    descriptionsdata = "test_description"
    etl_project_idsdata = 123

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "etl_project_id": etl_project_idsdata
           }

    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
        conn.commit()

    # Вызов функции подготовки БД для выполнения теста
    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() != None, "В БД добавлен проект с некорректным типом данных"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["etl_project_id"][0] == "Значение etl project id должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 4)Тест на уникальность поля acronim и name +++++
def test_projects_add_unique_acronim_name():
    url = ip + '/projects/add'

    acronimsdata = "test_acronim"
    namesdata = "testname"

    acronimsdata_sec = "test_acronim"
    namesdata_sec = "test_name"

    body = {
        "acronim": acronimsdata,
        "name": namesdata
           }

    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata_sec,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata_sec, namesdata_sec,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata_sec, namesdata_sec,))
        conn.commit()

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() == None, "В БД добавлен проект не добавлен"

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть уникальным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 5)тест на значения None в ключах запроса +++++
def test_projects_add_none_values():
    url = ip + '/projects/add'

    acronimsdata = None
    namesdata = None
    descriptionsdata = None
    parent_idsdata = None
    etl_project_idsdata = None

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "parent_id": parent_idsdata,
        "etl_project_id": etl_project_idsdata
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть корректным строковым значением.", "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно быть корректным строковым значением.", "Неверное содержание message"
    assert requestdict["status"]["message"]["parent_id"][0] == "Значение parent id должно иметь корректное целочисленное значение.", "Неверное содержание message"
    assert requestdict["status"]["message"]["etl_project_id"][0] == "Значение etl project id должно быть корректным строковым значением.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 6)тест на пустой запрос +++++
def test_projects_add_null_request():
    url = ip + '/projects/add'

    body = {

           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name является обязательным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 1)Получение всех проектов(без параметров) или получение проектов по определенным параметрам +++++
def test_projects_get():
    url = ip + '/projects/get'

    acronimsdata = "test_acronim"
    namesdata = "test_name"

    cur = conn.cursor()

    # Проверить наличие и добавить запись с аттрибутами acronimsdata, namesdata
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))

    id_project = cur.fetchone()[0]

    body = {
        "project_ids": [id_project]
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["data"][0]["id"] == id_project, "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 3)Получение всех проектов(без параметров) или получение проектов по определенным параметрам ---Косяк не мой---
# Тест на запрос с 2 истинными и 1 ложным ключом
def test_projects_get_correct_and_incorrect_key():
    url = ip + '/projects/get'

    acronimsdata = "test_acronim"
    namesdata = "test_name"

    acronimsdata_second = "second_test_acronim"
    namesdata_second = "second_test_name"

    cur = conn.cursor()

    # Проверить наличие и добавить запись с аттрибутами acronimsdata, namesdata
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
        conn.commit()

    # Проверить наличие и добавить запись с аттрибутами acronimsdata_second, namesdata_second
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata_second, namesdata_second,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata_second, namesdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    id_project = cur.fetchone()[0]

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
    id_project_sec = cur.fetchone()[0]

    cur.execute("SELECT MAX(id) FROM " + table)
    ids_data = cur.fetchone()[0] + 100

    body = {
        "project_ids": [id_project, id_project_sec, ids_data]
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["data"][0]["id"] == id_project, "Не получен реальный проект"
    assert requestdict["data"][1]["id"] == id_project_sec, "Не получен реальный проект"
    assert requestdict["status"]["message"]["project_ids.2"][0] == "Выбранное значение project_ids.2 является неверным.", \
        "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# Узнать !!!
# 4)Получение всех проектов(без параметров) или получение проектов по определенным параметрам +++++
# Тест на превышение максимального количества знаков в значениях ключей
def test_projects_get_max_limit_values():
    url = ip + '/projects/get'

    acronimsdata = "zazjhtjhtjojhtjbgfhugihgtusrgjfjhtjsruthyjutjgfbghsuthjjytjgfsbuhguihutihyuisrnbguisfithuhsitusrhgturstuirshutgiu"

    body = {
        "acronims": [acronimsdata]
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["acronims.0"][1] == "Значение acronims.0 должно быть меньше или равно 50 символам." ,\
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 5)Получение всех проектов(без параметров) или получение проектов по определенным параметрам +++++
# Пустой запрос
def test_projects_get_null_request():
    url = ip + '/projects/get'

    body = {

           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM projects")
    assert (cur.fetchone()) != (len(requestdict["data"]),), \
        "Кол-во записей в БД не соответствует кол-ву записей которые мы отправили в запросе"
    assert response.status_code == 400, "Неверный код ответа"


# 6)Получение всех проектов(без параметров) или получение проектов по определенным параметрам +++++++
# None (null)
def test_projects_get_none_values():
    url = ip + '/projects/get'

    id_project = None

    body = {
        "project_ids": [id_project]
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["project_ids.0"][0] == "Значение project_ids.0 должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 8)Получение всех проектов(без параметров) или получение проектов по определенным параметрам +++++
# Тест на запрос без массива
def test_projects_get_without_array():

    url = ip + '/projects/get'

    acronimsdata = "test_acronim"
    namesdata = "test_acronim"
    descriptionsdata = "description"

    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))

    id_project = cur.fetchone()[0]

    body = {
        "project_ids": id_project
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["project_ids"][0] == "Значение project ids должно быть массивом.", \
                "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 9)Получение всех проектов (без параметров) или получение проектов по определенным параметрам +++++
# Тест на запрос с 2 ложными ключами
def test_projects_get_incorrect_key():
    url = ip + '/projects/get'

    cur = conn.cursor()

    cur.execute("SELECT MAX(id) FROM " + table)
    ids_data = cur.fetchone()[0] + 10

    cur.execute("SELECT MAX(id) FROM " + table)
    ids_data_sec = cur.fetchone()[0] + 100

    body = {
        "project_ids": [ids_data, ids_data_sec]
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["project_ids.0"][0] == "Выбранное значение project_ids.0 является неверным.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["project_ids.1"][0] == "Выбранное значение project_ids.1 является неверным.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 1)Обновление проекта +++++
def test_projects_update():
    url = ip + '/projects/update'

    acronimsdata = "test_acronim"
    namesdatabefore = "test_name_before"
    namesdata = "test_name"
    descriptionsdatabefore = "test_description_before"
    descriptionsdata = "test_description"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdatabefore,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)",
                    (acronimsdata, namesdatabefore, descriptionsdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие обновленного показателя
    cur.execute("SELECT * FROM " + table + " WHERE description = %s AND name = %s", (descriptionsdata, namesdata,))
    assert cur.fetchone() != None, "В БД строка НЕ изменилась!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 2)Обновление проекта (пустое обновление) +++++
def test_projects_update_null_request():
    url = ip + '/projects/update'

    body = {

           }

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно присутствовать" \
                                                                 " и иметь непустое значение," \
                                                                 " если все из name / description / parent id / etl project id отсутствуют.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 3)Обновление проекта (None) +++++
def test_projects_update_none_values():
    url = ip + '/projects/update'

    acronimsdata = "test_acronim"
    namesdatabefore = "test_name_before"
    namesdata = None
    descriptionsdata = "description"

    body = {
        "acronim": acronimsdata,
        "name": namesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdatabefore,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)", (acronimsdata, namesdatabefore, descriptionsdata))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие обновленного показателя
    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    assert cur.fetchone() == None, "В БД строка обнулилась (None)"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 4)Обновление проекта +++++
# Тест на уникальность полей
def test_projects_update_unique_name():
    url = ip + '/projects/update'

    acronimsdata = "test_acronim"
    namesdata = "test_name"
    descriptionsdata = "description"

    acronimsdata_sec = "test_second_acronim"
    namesdatabefore = "test_name"
    descriptionsdatabefore = "description"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata_sec, namesdatabefore,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)",
                    (acronimsdata_sec, namesdatabefore, descriptionsdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие обновленного показателя
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    assert cur.fetchone() != None, "В БД добавилась строка name c таким же значением как в namesdatabefore!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Значение name является уникальным", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 6)Обновление проекта +++++
# Тест на превышение максимального количества знаков в значениях ключей
def test_projects_update_max_limit_values():
    url = ip + '/projects/update'

    acronimsdata = "test_acronim"
    namesdatabefore = "test_name"
    namesdata = "bbfidhohsjtojsbogjsiohtjiorsjbhoigjfsiojhtusryijhbigsjohtjisroyujhbgofjhiotgjrsyiohjbgiopjphuiosryjpiobjhrart"
    descriptionsdata = "qwejhytioejdhyiodpjhnhdjyhtdnjmyhtdmjhyktdkjnyhtkdjyhktdpjknyhptkdjpoythkdpjknyhptkdjnpyhktdpjkyphtkdjpy \n" \
                       "tkdjyoptdyiotdjhioysjdhigojsijgrteaiojhyiosjguifjdbioyhpjdiyhsgjpihjpsryjhpgyiobhgdhpsrirty"
    descriptionsdatabefore = "description"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdatabefore,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)",
                    (acronimsdata, namesdatabefore, descriptionsdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие обновленного показателя
    cur.execute("SELECT * FROM " + table + " WHERE name = %s AND description = %s", (namesdata, descriptionsdata))
    assert cur.fetchone() == None, "В БД добавилась строки с превышением допустимого кол-ва знаков!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть меньше или равно 80 символам.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно быть меньше или равно 80 символам.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 8)Обновление проекта +++++
# # Тест на запрос с некорректными типами передаваемых данных в значениях ключей
def test_projects_update_error_key_value():
    url = ip + '/projects/update'

    acronimsdata = "test_acronim"
    namesdatabefore = "test_name"
    namesdata = 128

    body = {
        "acronim": acronimsdata,
        "name": namesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdatabefore,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdatabefore,))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие обновленного показателя
    cur.execute("SELECT * FROM " + table + " WHERE name = $", (namesdata,))
    assert cur.fetchone() != None, "В БД поле name Обновилась на некорректный тип данных!"

    # # Проверка БД на наличие обновленного показателя
    # cur.execute("SELECT * name = CAST(name as int) FROM " + table + " WHERE name = %s", (namesdata,))
    # assert cur.fetchone() != None, "В БД поле name Обновилась на некорректный тип данных!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 1)Удаление проектов по акрониму (положительное тестирование) +++++
def test_projects_delete():
    url = ip + '/projects/delete'

    acronimsdata = "test_name"
    namesdata = "test_name"
    descriptionsdata = "description"
    acronimsdata_sec = "test_second_acronim"
    namesdata_sec = "test_second_name"
    descriptionsdata_sec = "test_description"

    body = {
        "acronims": [acronimsdata, acronimsdata_sec]
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия аттрибутов acronimsdata и namesdata в БД и добавление записи
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)", (acronimsdata, namesdata, descriptionsdata))
        conn.commit()

    # Проверка наличия аттрибутов acronimsdata_sec и namesdata_sec в БД и добавление записи
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata_sec,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description) VALUES (%s, %s, %s)", (acronimsdata_sec, namesdata_sec, descriptionsdata_sec))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() != None, "В БД проект не удалился!"
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata_sec, namesdata_sec))
    assert cur.fetchone() != None, "В БД проект не удалился!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 2)Удаление проектов по акрониму (пустое удаление) +++++
def test_projects_delete_null_request():
    url = ip + '/projects/delete'

    body = {

           }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims является обязательным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 3)Удаление проектов по акрониму (None) +++++
def test_projects_delete_none():
    url = ip + '/projects/delete'

    acronimsdata = None

    body = {
        "acronims": [acronimsdata]
            }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Значение acronims.0 должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 4)Удаление проектов по несуществующему акрониму +++++
def test_projects_delete_incorrect_key():
    url = ip + '/projects/delete'

    acronimsdata = "test_acronim"
    namesdata = "test_name"

    body = {
        "acronims": [acronimsdata]
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() != None, "В БД проект не удалился!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.",\
                                                                "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 5)Удаление проектов по акрониму (положительное тестирование) +++++
# #  Тест на указание 1 ложного и 1 истинного значений ключа
def test_projects_delete_correct_and_incorrect_key():
    url = ip + '/projects/delete'

    acronimsdata = "test_acronim"
    namesdata = "test_name"

    acronimsdata_sec = "test_incorrect_acronim"

    body = {
        "acronims": [acronimsdata, acronimsdata_sec]
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() == None, "В БД проект не добавился!"

    # Проверка БД на наличие удаленного проекта
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    assert cur.fetchone() != None, "В БД проект не удалился!"

    assert requestdict["status"]["message"]["acronims.1"][0] == "Выбранное значение acronims.1 является неверным.", \
                                                                       "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 6)Удаление проектов по акрониму (положительное тестирование) +++++
# # Тест на запрос без массива
def test_projects_delete_without_array():
    url = ip + '/projects/delete'

    acronimsdata = "test_acronim"
    namesdata = "test_name"

    body = {
        "acronims": acronimsdata
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
    if cur.fetchone() != None:
        cur.execute("INSERT INTO " + table + " (acronim, name) VALUES (%s, %s)", (acronimsdata, namesdata,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    assert cur.fetchone() != None, "В БД проект НЕ добавлен!"

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims должно быть массивом.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 8)Удаление проектов по акрониму (положительное тестирование) +++++
# #  Тест на запрос с некорректными типами передаваемых данных в значениях ключей
def test_projects_delete_error_type_values():
    url = ip + '/projects/delete'

    acronimsdata = 128

    body = {
        "acronims": [acronimsdata]
           }

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Значение acronims.0 должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 9)Удаление проектов по акрониму (положительное тестирование) +++++
# # Тест на превышение максимального количества знаков в значениях ключей
def test_projects_delete_max_limit_values():
    url = ip + '/projects/delete'

    acronimsdata = "pumgjonhotjrsohbjgofjshtiojsrhyjrosbjhgorjshsrthobrgtjsojhytiosrjhiogjsoirgjtiosjhyiojshugjshuojtruiosjhtuiosrjba"

    body = {
        "acronims": [acronimsdata]
           }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["acronims.0"][1] == "Значение acronims.0 должно быть меньше или равно 30 символам.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"
# #
# #
# #
# #
# # Закрытие подключения к БД по SSH
def test_stopserver():
    stop(conn, server)


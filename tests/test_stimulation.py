import btoken
import requests
import json
import db

headers = btoken.get_token()
ip="http://192.168.77.116"
start = db.startdb
stop = db.stopdb

# БД
table = "stimulation_grounds"
table_sec = "project_attributes"
table_tr = "project_user"
table_fouth = "projects_services"
table_users = "users"
table_services = "services"
table_projects_services = "projects_services"


# Старт подключения к БД по SSH
def test_startserver():
    global conn, server
    conn, server = start()


# # 1)Положительное тестирование, Добавление нового штрафа/бонуса +++++
def test_stimulation_add():
    url = ip + '/stimulation/add'

    acronimsdata = "zazu"
    namesdata = "homer"
    descriptionsdata = "qwerty"
    typesdata = "1"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s OR name = %s",
                (acronimsdata, namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s OR name = %s", (acronimsdata, namesdata,))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно создано", "Неверное содержание message"
    assert response.status_code == 201, "Неверный код ответа"
#
#
#
# # 2)Добавление нового штрафа/бонуса с превышением допустимого кол-ва знаков +++++
def test_stimulation_add_max_limit_values():
    url = ip + '/stimulation/add'

    acronimsdata = "zazуккпреыорпеоыгорипареырзоепщкшызропеыегрокпгшщызошпщзаоргокызроегзкыпзаыргезоргныорпазывпегu"
    namesdata = "hoатыпшгеыршрпшытпгешзуырфпавтмавфзтпкегшргшнтавыпегогрроыпшзмтаозвыштпгшзыетрзыкешрзшыкертзыкеmer"
    descriptionsdata = "qwertтмоаgohriotjrpogfodhsgtpuioghvfjdshgtihevihsfuiodhguiotrehvosfhduioghtuioevhuiosfdhgtuiorhevuiofhdsuioghtuioevhfuidshguithrevuihfdsuighstieторгкншузтрнгшктриапоывтмзвфтргзктршзртиыкпотипаолдытиазфптегзтрнзкгшытипаошытимаy"
    typesdata = "1478165782431657824656556478356921675496543659263759745647836578241657796478356478564781"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == 'Значение acronim должно быть меньше или равно 30 символам.',\
        "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == 'Значение name должно быть меньше или равно 50 символам.', \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == 'Значение description должно быть меньше или равно 150 символам.', \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["type"][0] == 'Значение type должно быть меньше или равно 1 символам.', \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 3)Добавление штрафа/бонуса с некорректным типом данных +++++
def test_stimulation_add_error_type_values():
    url = ip + '/stimulation/add'

    acronimsdata = 128
    namesdata = 128
    descriptionsdata = "description"
    typesdata = 1

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Вызов функции подготовки БД для выполнения теста
    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["type"][0] == "Значение type должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 4)Тест на уникальность поля acronim и name штрафа/бонуса +++++
def test_stimulation_add_unique_acronim_name():
    url = ip + '/stimulation/add'

    acronimsdata = "zazu"
    namesdata = "homer"
    descriptionsdata = "qwerty"
    typesdata = "1"

    acronimsdata_sec = "zazu"
    namesdata_sec = "homer"
    descriptionsdata_sec = "qwerty"
    typesdata_sec = "1"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s OR name = %s",
                (acronimsdata_sec, namesdata_sec,))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata_sec, namesdata_sec, descriptionsdata_sec, typesdata_sec))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim должно быть уникальным.", "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть уникальным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 5)тест на значения None в ключах запроса штрафа/бонуса +++++
def test_stimulation_add_none_values():
    url = ip + '/stimulation/add'

    acronimsdata = None
    namesdata = None
    descriptionsdata = None
    typesdata = None

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name является обязательным.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["type"][0] == "Значение type является обязательным.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 6)тест на пустой запрос штрафа/бонуса +++++
def test_stimulation_add_null_request():
    url = ip + '/stimulation/add'

    body = {

           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
    assert requestdict["status"]["message"]["name"][0] == "Значение name является обязательным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 1)Получение все штрафов или бонусов +++++
def test_stimulation_get():
    url = ip + '/stimulation/get'

    acronimsdata = "zazu"
    namesdata = "buzova"
    descriptionsdata = "description"
    typesdata = "1"

    body = {
        "type": typesdata
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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["data"][0]["acronim"] == acronimsdata, "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 2)Получение всех штрафов или бонусов ---Косяк не мой---
# Тест на запрос с 2 истинными и 1 ложным ключом
def test_stimulation_get_correct_and_incorrect_key():
    url = ip + '/stimulation/get'

    acronimsdata = "zazu"
    namesdata = "buzova"
    descriptionsdata = "desc"
    typesdata = "1"

    acronimsdata_second = "joker"
    namesdata_second = "kevin"
    descriptionsdata_second = "desc"
    typesdata_second = "2"

    acronimsdata_incorrect = "spawn"
    namesdata_incorrect = "harry"
    descriptionsdata_incorrect
    typesdata_incorrect = "3"

    body = {
        "types": [typesdata, typesdata_second, typesdata_incorrect]
           }

    cur = conn.cursor()

    # Проверка наличия и добавления первой записи в БД с аттрибутами: acronimsdata, namesdata, descriptionsdata, typesdata
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata))
        conn.commit()

    # Проверка наличия и добавления второй записи в БД с аттрибутами: acronimsdata_second, namesdata_second, descriptionsdata_second, typesdata_second
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                (acronimsdata_second, namesdata_second, descriptionsdata_second, typesdata_second))
        conn.commit()

    # Проверка наличия и удаления третьей записи в БД с аттрибутами: acronimsdata_incorrect, namesdata_incorrect, descriptionsdata_incorrect, typesdata_incorrect
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata_second,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata_second,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                (acronimsdata_second, namesdata_second, descriptionsdata_second, typesdata_second))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["data"][0]["type"] == typesdata, "Не получен реальный проект"
    assert requestdict["data"][1]["type"] == typesdata_second, "Не получен реальный проект"
    assert requestdict["data"][2]["type"] == "Выбранное значение types.2 является неверным", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 3)Получение все штрафов или бонусов +++++
# Тест на превышение максимального количества знаков в значениях ключей
def test_stimulation_get_max_limit_values():
    url = ip + '/stimulation/get'

    typesdata = "1214231542347698665421657856546547653765375426575426752465276536546536542652675376547564365245654736547654867545643"

    body = {
        "type": typesdata
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["type"][0] == "Значение type должно быть меньше или равно 1 символам.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 5)Получение все штрафов или бонусов +++++
# Пустой запрос
def test_stimulation_get_null_request():
    url = ip + '/stimulation/get'

    body = {

           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM projects")
    assert (cur.fetchone()) != (len(requestdict["data"]),)
    assert response.status_code == 400, "Неверный код ответа"


# 6)Получение все штрафов или бонусов +++++++
# None (null)
def test_stimulation_get_none_values():
    url = ip + '/stimulation/get'

    typesdata = None

    body = {
        "type": typesdata
           }

    response = requests.post(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["type"][0] == "Значение type является обязательным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 7)Получение все штрафов или бонусов которых нет в БД +++++
def test_stimulation_get_incorrect_key():
    url = ip + '/stimulation/get'

    typesdata = "3"

    body = {
        "type": typesdata
    }

    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE type = %s", (typesdata,))
    if cur.fetchone() != None:
        print("Тестовые данные найдены в БД, получение")
        cur.execute("DELETE FROM " + table + " WHERE type = %s", (typesdata,))
        conn.commit()

    response = requests.post(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Запись не найдена", \
            "Неверное содержание message"
    assert response.status_code == 404, "Неверный код ответа"


# 1)Обновление штрафа/бонуса +++++Метод PUT не работает+++++
def test_stimulation_update():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    namesdatabefore = "nina"
    namesdata = "bart"
    descriptionsdatabefore = "description"
    descriptionsdata = "qwerty"
    typesdatabefore = "1"
    typesdata = "3"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия и добавления записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdatabefore, descriptionsdatabefore, typesdatabefore))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 2)Обновление штрафа/бонуса (пустое обновление) +++
def test_stimulation_update_null_request():
    url = ip + '/stimulation/update'

    body = {

           }

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronim"][0] == "Значение acronim является обязательным.", "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно присутствовать и иметь непустое значение," \
                                                                 " если все из name / description / type отсутствуют.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"
#

# 3)Обновление штрафа/бонуса (None) +++++
def test_stimulation_update_none_acronim_name():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    namesdatabefore = "nina"
    namesdata = None
    descriptionsdatabefore = "description"
    descriptionsdata = None
    typesdatabefore = "1"
    typesdata = None

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Проверка наличия и добавления записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdatabefore, descriptionsdatabefore, typesdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно присутствовать и иметь непустое значение, " \
                                                                 "если все из name / description / type отсутствуют.", \
            "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 4)Обновление штрафа/бонуса +++++
# Тест на уникальность полей
def test_stimulation_update_unique_acronim_name():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    acronimsdatabefore = "venom"
    namesdata = "bart"
    namesdatabefore = "bart"
    descriptionsdata = "description"
    typesdata = "1"
    typesdatabefore = "2"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия и добавления записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdatabefore, namesdatabefore))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdatabefore, namesdatabefore, descriptionsdatabefore, typesdatabefore))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (acronimsdata,))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть уникальным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 5)Обновление штрафа/бонуса +++++
# Тест на обнуление данных при обновлении
def test_stimulation_update_none_type_name():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    namesdatabefore = "nina"
    descriptionsdata = "desc"
    namesdata = None
    typesdata = None
    typesdatabefore = "1"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "type": typesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия и добавления записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdatabefore))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdatabefore, namesdatabefore, descriptionsdata, typesdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 6)Обновление штрафа/бонуса +++++
# Тест на превышение максимального количества знаков в значениях ключей
def test_stimulation_update_max_limit_values():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    namesdatabefore = "nina"
    namesdata = "bbfidhohsjtojsbogjsiohtjiorsjbhoigjfsiojhtusryijhbigsjohtjisroyujhbgofjhiotgjrsyiohjbgiopjphuiosryjpiobjhrart"
    descriptionsdata = "qwejhytioejdhyiodpjhnhdjyhtdnjmyhtdmjhyktdkjnyhtkdjyhktdpjknyhptkdjpoythkdpjknyhptkdjnpyhktdpjkyphtkdjpytkdjyoptdyiotdjhioysjdhigojsijgrteaiojhyiosjguifjdbioyhpjdiyhsgjpihjpsryjhpgyiobhgdhpsrirty"
    typesdata = "1478165782431657824656556478356921675496543659263759745647836578241657796478356478564781"
    typesdatabefore = "1"
    descriptionsdatabefore = "desc"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "description": descriptionsdata,
        "type": typesdata
           }

    # Подготовка БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия и добавления записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdatabefore,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdatabefore,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdatabefore))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdatabefore, namesdatabefore, descriptionsdata, typesdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть меньше или равно 50 символам.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["description"][0] == "Значение description должно быть меньше или равно 150 символам.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 7)Обновление штрафа/бонуса +++++
# # Тест на запрос с некорректными типами передаваемых данных в значениях ключей
def test_stimulation_update_error_type_values():
    url = ip + '/stimulation/update'

    acronimsdata = "zazu"
    namesdatabefore = "nina"
    namesdata = 128
    typesdata = 1
    typesdatabefore = "1"
    descriptionsdata = "desc"

    body = {
        "acronim": acronimsdata,
        "name": namesdata,
        "type": typesdata
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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s",
                (acronimsdata, namesdatabefore))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdatabefore, namesdatabefore, descriptionsdata, typesdatabefore))
        conn.commit()

    # Запрос на обновление показателя
    response = requests.put(url, json=body, headers=headers)
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["name"][0] == "Значение name должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert requestdict["status"]["message"]["type"][0] == "Значение type должно быть корректным строковым значением.", \
        "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 1)Удаление штрафов/бонусов (положительное тестирование)
# +++++Метод DELETE не работает, работает только с POST++++
def test_stimulation_delete():
    url = ip + '/stimulation/delete'

    acronimsdata = "pumba"
    namesdata = "katrin"
    descriptionsdata = "desc"
    typesdata = "1"

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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() == None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"] == "Успешно", "Неверное содержание message"
    assert response.status_code == 200, "Неверный код ответа"


# 2)Удаление штрафов/бонусов (пустое удаление) +++
def test_stimulation_delete_null_request():
    url = ip + '/stimulation/delete'

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


# 3)Удаление штрафов/бонусов по акрониму (None) +++++
def test_stimulation_delete_none_values():
    url = ip + '/stimulation/delete'

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
    assert requestdict["status"]["message"]["acronims.0"][0] == "Значение acronims.0 является обязательным.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 4)Удаление штрафов/бонусов по несуществующему акрониму +++++
def test_stimulation_delete_incorrect_key():
    url = ip + '/stimulation/delete'

    acronimsdata = "zazu"
    namesdata = "katrin"
    descriptionsdata = "desc"
    typesdata = "1"

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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() != None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims.0"][0] == "Выбранное значение acronims.0 является неверным.",\
                                                                "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# # 5)Удаление штрафов/бонусов по акрониму (положительное тестирование) -------Косяк не мой-------
# #  Тест на указание 1 ложного и 1 истинного значений ключа
def test_stimulation_delete_correct_and_incorrect_key():
    url = ip + '/stimulation/delete'

    acronimsdata = "zazu"
    namesdata = "katrin"
    descriptionsdata = "desc"
    typesdata = "1"

    acronimsdata_sec = "venom"

    body = {
        "acronims": [acronimsdata, acronimsdata_sec]
           }

    # Вызов функции подготовки БД для выполнения теста
    cur = conn.cursor()

    # Проверка наличия и добавления истинной записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE name = %s", (namesdata,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE name = %s", (namesdata,))
        conn.commit()

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() != None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata,))
        conn.commit()

    #Проверка наличия и удаления ложной записи в БД
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
    if cur.fetchone() != None:
        cur.execute("DELETE FROM " + table + " WHERE acronim = %s", (acronimsdata_sec,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверка БД на наличие добавленного проекта
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s", (acronimsdata,))
    assert cur.fetchone() == None, "Не удален"
    assert requestdict["status"]["message"]["acronims.1"][0] == "Выбранное значение acronims.1 является неверным.", \
                                                                       "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 6)Удаление штрафов/бонусов по акрониму +++++
# Тест на запрос без массива
def test_stimulation_delete_without_array():
    url = ip + '/stimulation/delete'

    acronimsdata = "zazu"
    namesdata = "katrin"
    descriptionsdata = "desc"
    typesdata = "1"

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

    cur.execute("SELECT * FROM " + table + " WHERE acronim = %s AND name = %s", (acronimsdata, namesdata))
    if cur.fetchone() != None:
        cur.execute("INSERT INTO " + table + " (acronim, name, description, type) VALUES (%s, %s, %s, %s)",
                    (acronimsdata, namesdata, descriptionsdata, typesdata,))
        conn.commit()

    response = requests.delete(url, json=body, headers=headers)  # Запрос на добавление проекта
    assert response.status_code != 500, "Ошибка от laravel"
    assert response.status_code != 405, "Ошибка метода отправки"
    requestdict = json.loads(response.content)

    # Проверки на содержание message и верный статус код
    assert requestdict["status"]["message"]["acronims"][0] == "Значение acronims должно быть массивом.", "Неверное содержание message"
    assert response.status_code == 400, "Неверный код ответа"


# 8)Удаление штрафов/бонусов по акрониму (положительное тестирование) +++++
# Тест на запрос с некорректными типами передаваемых данных в значениях ключей
def test_stimulation_delete_error_type_values():
    url = ip + '/stimulation/delete'

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


# 9)Удаление штрафов/бонусов по акрониму +++++
# Тест на превышение максимального количества знаков в значениях ключей
def test_stimulation_delete_max_limit_values():
    url = ip + '/stimulation/delete'

    acronimsdata = "pumgjonhotjrsohbjgofjshtiojsrhyjrosbjhgorjshsrthobrgtjsojhytiosrjhiogjsoirgjtiosjhyiojshugjshuojtruiosjhtuiosrjba"

    body = {
        "acronims": [acronimsdata]
           }

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


# Закрытие подключения к БД по SSH
def test_stopserver():
    stop(conn, server)


## Приложение для "ДОМ РФ"  

### Описание  

У приложения есть два эндпойнта:  
- POST /calc/
- GET /result/

Для POST /calc/ в тело запроса надо передать:  
```
{
    "cadastral_number": "10:00:000000:00", 
    "latitude": 54.1231, 
    "longitude": 37.1231
}
```  

Запрос записывается в БД и в ответ сразу же возвращается ID запроса по которому клиент будет запрашивать результат.  

Под капотом, реализуемый сервис отправляет запрос на расчет внешнему сервису (Самого сервиса нет, происходит эмуляция  
работы сервиса, который может выполнять расчет 10-20 секунд). В ответе от сервиса приходит «скор».  
После расчета результат сохраняется в БД и доступен для инициатора.  

Для GET /result/{request_id} в запросе нужно передать id запроса который вернул POST /calc/ и в ответ придет `scor` и  
статус вычислений.  

Например, если `scor` уже посчитан, то ответ будет:  

```
{
  "score": -13.40412,
  "status": "completed"
}
```

А если процесс расчета еще не завешен, то такой:  

```
{
  "score": null,
  "status": "in progress"
}
```

### Запуск  

1) Клонируйте репозиторий к себе на ПК.  

```
git clone https://github.com/AleksSpace/for_dom_rf.git
```

2) Перейдите в директорию, в которую клонировали проект, а затем установите и активируйте виртуальное окружение.  

3) Заполните файл .env (пример заполнения показан в файле .env.example)

4) Установите зависимости командой:  

```
pip install -r requirements.txt
```

5) Запустите миграции командой:  

```
alembic -c src/alembic.ini upgrade head
```

6) Перейдите в директорию src и запустите проект командой:  

```
python main.py
```

7) По адресу http://127.0.0.1:8000/docs#/ откройте интерактивную документацию и проверьте эндпойнты.


### Запуск через Docker compose  

1) Клонируйте репозиторий к себе на ПК.  

```
git clone https://github.com/AleksSpace/for_dom_rf.git
```

2) Перейдите в директорию, в которую клонировали проект

3) Заполните файл .env (пример заполнения показан в файле .env.example)

4) В файле docker-compose.yaml в сервисе db пропишите ваши подключения к БД в переменных:  
- POSTGRES_USER  
- POSTGRES_PASSWORD  
- POSTGRES_DB  

5) Запустите docker compose:  

```
docker compose up --build
```

Приложение развернётся и запустится в контейнере. 

6) По адресу http://0.0.0.0:8000/docs#/ откройте интерактивную документацию и проверьте эндпойнты.

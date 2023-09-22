# Tg_agregator
### Clone project and enter in the infra folder:
```bash
git clone https://github.com/Imwisagist/Test_for_Reliable_Loyal_Technologies.git && cd Test_for_Reliable_Loyal_Technologies/infra
```
### Create a .env file in infra folder and enter the token of your telegram bot into it:
```bash
nano .env
TELEGRAM_BOT_TOKEN = <TOKEN>
```
### Run docker-compose:
```bash
docker-compose up -d
```
### Fill in the database:
```bash
winpty docker exec -it fastapi_backend bash -c "poetry run python load_data.py"
```
### Go to the Telegram, write to your bot and enjoy!)
### How it looks:
![screenshot](https://github.com/imwisagist/Test_for_Reliable_Loyal_Technologies/blob/main/other/how_it_looks.jpg?raw=true)
### **Test task description:**
<details>
    <summary>Click to show</summary>
Ваш алгоритм должен принимать на вход:
Дату и время старта агрегации в ISO формате (далее dt_from)
Дату и время окончания агрегации в ISO формате (далее dt_upto)
Тип агрегации (далее group_type). Типы агрегации могут быть следующие: hour, day, month. То есть группировка всех данных за час, день, неделю, месяц.


Пример входа:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}


Комментарий к входным данным: вам необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, тип агрегации по месяцу


На выходе ваш алгоритм формирует ответ содержащий:
Агрегированный массив данных (далее dataset)
Подписи к значениям агрегированного массива данных в ISO формате (далее labels)


Пример ответа:
{"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}


После разработки алгоритма агрегации, вам необходимо создать телеграм бота, который будет принимать
от пользователей текстовые сообщения содержащие JSON с входными данными и отдавать агрегированные данные
в ответ. Посмотрите @rlt_testtaskexample_bot - в таком формате должен работать и ваш бот.
</details>

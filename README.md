# Countries telegram bot

### Description:
The Countries telegram bot was written during team internship in [Y_lab](https://ylab.io/).  
This bot allows you to get info about any country: 
- capital,
- population,
- area size,
- national languages,
- national currencies,
- current weather in capatal.
You also can get info about any city:
- country,
- current weather in the city.


### Requirements:
1. MacOS (prefer) / Linux / Windows10
2. `Docker`
3. `Poetry`
4. `Make` utily for MacOS, Linux.

### Install:
1. Clone repository: https://github.com/sergkim13/countries_telegram_bot
2. Create `.env` and fill it up according to `.envexample`.
3. Type `make install` to install dependencies.
4. Type `make compose` for running application in docker container. Type `make stop` to stop app container.


### **Task description**
<details>
    <summary>Click to show</summary>

### Countries Informator Bot

Чат-бот для получения актуальной информации о стране
Задача
Получать актуальную информацию об указанной стране в чат-боте для Telegram: георафическую, языки, курсы валют, погода.
Требования
Должна быть возможность запроса сведений по городу (страна должна определяться автоматически). Все данные должны быть актуальными (периодически обновляемые в системе из открытых API). 

Использовать открытые API:
- для импорта информации о странах (обновлять редко);
- для импорта информации о погоде (обновлять часто);
- для импорта информации о курсах валют (обновлять часто).

Информация должна сохраняться в БД и иметь возможность её просмотра в панели управления.

В чат-боте для Telegram должен быть предусмотрен интерфейс с кнопочным меню для возможности запроса указанной информации.  
Технологический стек
- Docker
- Django 4.1 (async)
- PostgreSQL 15
- Celery
</details>


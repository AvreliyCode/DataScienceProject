from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Создание папки data, если она не существует
if not os.path.exists("data"):
    try:
        os.makedirs("data")
    except PermissionError:
        print("Ошибка: Нет прав на создание папки 'data'. Попробуйте запустить скрипт от имени администратора.")
        exit()

# Инициализация веб-драйвера
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)
driver.get('https://www.gismeteo.ru/weather-novosibirsk-4690/2-weeks/')

try:
    # Ожидание загрузки таблицы
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/section[2]/div[1]/div'))
    )

    # Прокрутка страницы для загрузки всех данных
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Даем время для загрузки данных

    # Сбор данных
    data = []

    # Задаем первую дату (сегодняшнюю дату)
    current_date = datetime.now()

    # Цикл по дням (14 дней)
    for day in range(1, 15):
        # Форматируем дату
        date_str = current_date.strftime("%d.%m.%Y")

        # Извлечение максимальной температуры
        max_temp_element = driver.find_element(By.XPATH, f'/html/body/main/div[1]/section[2]/div[1]/div/div/div[3]/div/div/div[{day}]/div[1]/temperature-value')
        max_temp = max_temp_element.text.strip()

        # Извлечение минимальной температуры
        min_temp_element = driver.find_element(By.XPATH, f'/html/body/main/div[1]/section[2]/div[1]/div/div/div[3]/div/div/div[{day}]/div[2]/temperature-value')
        min_temp = min_temp_element.text.strip()

        # Извлечение осадков
        precipitation_element = driver.find_element(By.XPATH, f'/html/body/main/div[1]/section[2]/div[1]/div/div/div[12]/div[{day}]/div[1]')
        precipitation = precipitation_element.text.strip()

        # Извлечение порывов ветра
        wind_gust_element = driver.find_element(By.XPATH, f'/html/body/main/div[1]/section[2]/div[1]/div/div/div[7]/div[{day}]/speed-value')
        wind_gust = wind_gust_element.text.strip()

        # Добавление данных в список
        data.append([date_str, max_temp, min_temp, precipitation, wind_gust])

        # Вывод данных в консоль для отладки
        print(f"День {day}: Дата={date_str}, Макс. температура={max_temp}, Мин. температура={min_temp}, Осадки={precipitation}, Ветер={wind_gust}")

        # Увеличиваем дату на 1 день
        current_date += timedelta(days=1)

    # Создание DataFrame
    df = pd.DataFrame(data, columns=["Дата", "Макс. температура", "Мин. температура", "Осадки", "Порывы ветра, м/c"])

    # Сохранение в Excel
    try:
        df.to_excel("data/weather_forecast.xlsx", index=False)
        print("Данные успешно сохранены в Excel!")
    except PermissionError:
        print("Ошибка: Нет прав на запись в файл 'data/weather_forecast.xlsx'. Убедитесь, что файл не открыт в другой программе.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

finally:
    # Закрытие браузера
    driver.quit()
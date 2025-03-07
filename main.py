import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
from config import *



# Ваш токен бота
TOKEN = tgtoken
bot = telebot.TeleBot(TOKEN)

# Параметры для входа на сайт
LOGIN_URL = url
USERNAME = uname
PASSWORD = passwrd

# Переменные для хранения информации о оценках
grades_info = ""
previous_grades_info = ""
algoritm_ocen = ""
previous_grades_infoA = ""

# Функция для входа на сайт и получения оценок
def login_to_site():
    global grades_info, previous_grades_info, algoritm_ocen, previous_grades_infoA  # Используем глобальные переменные для хранения оценок
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='/root/.cache/selenium/chromedriver/linux64/134.0.6998.35/chromedriver')
    options.add_argument('headless')  # Запуск в фоновом режиме без GUI
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(LOGIN_URL)

        # Найдите элементы для ввода логина и пароля и выполните вход
        username_input = driver.find_element(By.ID, 'username')  # Замените на правильный селектор
        password_input = driver.find_element(By.ID, 'password')  # Замените на правильный селектор

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        # Найдите кнопку входа и нажмите на нее
        login_button = driver.find_element(By.ID, 'loginbtn')  # Замените на правильный селектор
        login_button.click()

        time.sleep(3)  # Подождите, пока страница загрузится (можно использовать явные ожидания)

        # Проверяем, успешен ли вход по наличию элемента <h2 id="instance-336383-header">
        header_element = driver.find_element(By.ID, 'instance-336383-header')
        if header_element.text != "Личный кабинет":
            return False

        # Нажимаем на ссылку с href
        driver.find_element(By.XPATH, "//a[@href='https://moodle.inueco.ru/blocks/lk_inueco/lk_pages/current_grades.php?returnurl=https%3A%2F%2Fmoodle.inueco.ru%2Fmy%2Findex.php']").click()
        time.sleep(3)  # Подождите, пока страница загрузится

        # Нажимаем на кнопку с id "tabby-toggle_Uchebnyygod2024-2025"
        driver.find_element(By.ID, "tabby-toggle_Uchebnyygod2024-2025").click()
        time.sleep(3)  # Подождите, пока страница загрузится
        
        def click_element(driver, css_selector):
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            element.click()

        # Используем функцию для клика
        click_element(driver, 'td.clickable[data-closable_id="Uchebnyygod2024-2025_13"]')
        click_element(driver, 'td.clickable[data-closable_id="Uchebnyygod2024-2025_2"]')
                
        # Парсим информацию из элемента с id "Uchebnyygod2024-2025_13"
        grades_element = driver.find_element(By.ID, "Uchebnyygod2024-2025_13")
        grades_elementA = driver.find_element(By.ID, "Uchebnyygod2024-2025_2")


        # Получаем текст из элемента и разбиваем его по строкам
        grades_rows = grades_element.find_elements(By.TAG_NAME, 'tr')  # Получаем все строки таблицы
        grades_rowsA = grades_elementA.find_elements(By.TAG_NAME, 'tr')  # Получаем все строки таблицы

        # Формируем текст с разделением ячеек знаком "|"
        grades_text = []
        for row in grades_rows:
            cells = row.find_elements(By.TAG_NAME, 'td')  # Получаем все ячейки в строке
            row_data = ' | '.join(cell.text.strip() if cell.text.strip() else '+' for cell in cells)  # Заменяем пустые ячейки на '+'
            grades_text.append(row_data)
        grades_textA = []
        for row in grades_rowsA:
            cells = row.find_elements(By.TAG_NAME, 'td')  # Получаем все ячейки в строке
            row_data = ' | '.join(cell.text.strip() if cell.text.strip() else '+' for cell in cells)  # Заменяем пустые ячейки на '+'
            grades_textA.append(row_data)


        # Объединяем все строки в один текст
        current_grades_info = '\n'.join(grades_text).strip()  # Сохраняем информацию о оценках
        current_grades_infoA = '\n'.join(grades_textA).strip()  # Сохраняем информацию о оценках
       
        #Проверяем на измения в оценках по алгоритмизации
        if current_grades_infoA != previous_grades_infoA and previous_grades_infoA != "":
            if current_grades_info == "Отлично":
                        bot.send_message(chat_id, "Вам поставили 5 по алгоритмизации")  # Отправляем уведомление пользователю
            elif current_grades_info == "Хорошо":
                        bot.send_message(chat_id, "Вам поставили 4 по алгоритмизации")  # Отправляем уведомление пользователю
            elif current_grades_info == "Удовлетворительно":
                        bot.send_message(chat_id, "Вам поставили 3 по алгоритмизации")  # Отправляем уведомление пользователю
            elif current_grades_info == "Неудовлетворительно":
                        bot.send_message(chat_id, "Баланс поплнен по алгоритмизации!")  # Отправляем уведомление пользователю

        previous_grades_infoA = current_grades_infoA  # Обновляем предыдущее состояние оценок
        algoritm_ocen = current_grades_infoA  # Обновляем текущее состояние оценок

        # Проверяем на изменения в оценках по ПП
        if current_grades_info != previous_grades_info and previous_grades_info != "":
            if current_grades_info == "Отлично":
                        bot.send_message(chat_id, "Вам поставили 5 по прикладному программированию")  # Отправляем уведомление пользователю
            elif current_grades_info == "Хорошо":
                        bot.send_message(chat_id, "Вам поставили 4 по прикладному программированию")  # Отправляем уведомление пользователю
            elif current_grades_info == "Удовлетворительно":
                        bot.send_message(chat_id, "Вам поставили 3 по прикладному программированию")  # Отправляем уведомление пользователю
            elif current_grades_info == "Неудовлетворительно":
                        bot.send_message(chat_id, "Баланс поплнен по прикладному программированию!")  # Отправляем уведомление пользователю

        previous_grades_info = current_grades_info  # Обновляем предыдущее состояние оценок
        grades_info = current_grades_info  # Обновляем текущее состояние оценок
                

    except Exception as e:
        print(f'Ошибка при входе или парсинге: {e}')
    finally:
        driver.quit()  # Закрываем браузер

# Функция для пассивного парсинга каждые 30 секунд
def passive_parsing():
    while True:
        login_to_site()  # Выполняем парсинг оценок
        time.sleep(30)  # Ждем 30 секунд перед следующим парсингом

#Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    global chat_id  # Глобальная переменная для хранения ID чата
    chat_id = message.chat.id  # Сохраняем ID чата пользователя

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тягомотина")
    btn2 = types.KeyboardButton("Узнать оценки")
    markup.add(btn1, btn2)

    bot.send_message(chat_id, text="Бот для парсинга оценок ^_^ , {0.first_name}! ".format(message.from_user), reply_markup=markup)

# Словарь для отслеживания количества повторений сообщений
user_messages_count = {}

#Обработка команд
@bot.message_handler(func=lambda message: True)
def bot_response(message):
    user_id = message.from_user.id
    user_input = message.text.lower()
    
    # Создаем уникальный ключ для пользователя и его сообщения
    key = (user_id, user_input)

    # Увеличиваем счетчик сообщений
    if key in user_messages_count:
        user_messages_count[key] += 1
    else:
        user_messages_count[key] = 1

    # Проверяем количество повторений
    if user_messages_count[key] == 3:  # Например, если сообщение повторяется 3 раза
        bot.reply_to(message, f"Хватит уже тягомотить, {message.from_user.first_name}!")
    elif user_messages_count[key] > 3:
        bot.reply_to(message, f"Будешь и дальше тягомотить двойка на баланс залетит")
        # Можно сбросить счетчик, если хотите
        user_messages_count.pop(key)  # Удаляем запись после достижения определенного количества
    else:
        if user_input == "тягомотина":
            bot.reply_to(message, f"Ну ты и тягомот, {message.from_user.first_name}!")
        
        elif user_input == "узнать оценки":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Прикладное программирование")
            btn2 = types.KeyboardButton("Алгоритмизация")
            btn3 = types.KeyboardButton("Назад")
            markup.add(btn1, btn2, btn3)

            bot.send_message(message.chat.id, "Выбирай предмет:", reply_markup=markup)

        elif user_input == "прикладное программирование":
            bot.reply_to(message, f"Оценки по Прикладному программированию: \n{grades_info}")
        elif user_input == "алгоритмизация":
            bot.reply_to(message, f"Оценки по Алгоритмизации: \n{algoritm_ocen}")
        elif user_input == "назад":
            start(message)  # Возвращаемся к главному меню
        else:
            bot.reply_to(message, "Я не понимаю эту команду. Выберите одну из доступных опций.")

# Запуск потока для пассивного парсинга
parsing_thread = threading.Thread(target=passive_parsing)
parsing_thread.daemon = True  # Делаем поток демоном, чтобы он завершился при выходе основного потока
parsing_thread.start()

# Запуск бота
bot.polling(none_stop=True)

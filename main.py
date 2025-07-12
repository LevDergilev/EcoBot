import telebot
import requests
import random
import os
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokenid import token

bot = telebot.TeleBot(token)

# База знаний с ответами на частые вопросы
KNOWLEDGE_BASE = {
    # Основные понятия
    "глобальное потепление": {
        "source": "Глобальное потепление",
        "custom_answer": None
    },
    "экология": {
        "source": "Экология",
        "custom_answer": None
    },
    "парниковый эффект": {
        "source": "Парниковый эффект",
        "custom_answer": None
    },
    "изменение климата": {
        "source": "Изменение климата",
        "custom_answer": None
    },
    
    # Причины и последствия
    "причины глобального потепления": {
        "custom_answer": """Основные причины глобального потепления:
1. Сжигание ископаемого топлива (уголь, нефть, газ)
2. Вырубка лесов (деревья поглощают CO₂)
3. Промышленные выбросы
4. Интенсивное животноводство
5. Использование фреонов и других химических веществ"""
    },
    "какие последствия глобального потепления": {
        "custom_answer": """Возможные последствия:
🌡 Повышение средней температуры на планете
🌊 Таяние ледников и повышение уровня моря
🔥 Учащение экстремальных погодных явлений
🌍 Изменение экосистем и вымирание видов
🍃 Ухудшение качества воздуха
🌾 Проблемы с сельским хозяйством"""
    },
    
    # Решения и улучшения
    "как улучшить экологию": {
        "custom_answer": """Способы улучшения экологии:
1. ♻️ Сортировка и переработка мусора
2. 💡 Использование энергосберегающих технологий
3. 🌱 Поддержка возобновляемой энергетики
4. 🚶 Передвижение пешком или на велосипеде
5. 🛒 Осознанное потребление"""
    },
    "как бороться с глобальным потеплением": {
        "custom_answer": """Меры борьбы:
• Сокращение выбросов CO₂
• Переход на ВИЭ (солнечная, ветровая энергия)
• Энергоэффективные технологии
• Сохранение и восстановление лесов
• Поддержка экологических инициатив"""
    },
    
    # Конкретные вопросы
    "что такое углеродный след": {
        "source": "Углеродный след",
        "custom_answer": None
    },
    "альтернативные источники энергии": {
        "source": "Возобновляемая энергия",
        "custom_answer": None
    },
    "как сократить углеродный след": {
        "custom_answer": """Способы сокращения:
1. Летайте меньше - выбирайте поезда
2. Экономьте электроэнергию
3. Покупайте местные продукты
4. Уменьшите потребление мяса
5. Используйте многоразовые вещи вместо одноразовых"""
    },
    
    # Дополнительные темы
    "озоновые дыры": {
        "source": "Озоновая дыра",
        "custom_answer": None
    },
    "киотский протокол": {
        "source": "Киотский протокол",
        "custom_answer": None
    },
    "парижское соглашение": {
        "source": "Парижское соглашение",
        "custom_answer": None
    },
    "экологические организации": {
        "custom_answer": """Известные экологические организации:
• Greenpeace
• Всемирный фонд дикой природы (WWF)
• Гринпис
• Международный союз охраны природы
• ООН-Окружающая среда"""
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение с примерами вопросов"""
    welcome_text = """🌍 Привет! Я EcoLev_Bot. Могу рассказать о:
    
🔹 Глобальном потеплении и изменении климата
🔹 Экологических проблемах и решениях
🔹 Устойчивом развитии и защите природы

Примеры вопросов:
• Что такое парниковый эффект?
• Каковы причины глобального потепления?
• Как сократить углеродный след?
• Какие есть экологические организации?
• Какие последствия глобального потепления?
• Какие способы улучшения экологии?
• как бороться с глобальным потеплением?

Также можете отправить команду /image для получения случайного изображения с инфорамцией о глобальном потеплении.

Задайте ваш вопрос о экологии или глобальном потеплении!"""
    await update.message.reply_text(welcome_text)

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /image для отправки случайного изображения"""
    # Проверяем, существует ли папка с изображениями
    if not os.path.exists('images') or not os.path.isdir('images'):
        await update.message.reply_text("Папка с изображениями не найдена!")
        return
    
    # Получаем список файлов в папке
    images = [f for f in os.listdir('images') if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not images:
        await update.message.reply_text("В папке нет изображений!")
        return
    
    # Выбираем случайное изображение
    random_image = random.choice(images)
    image_path = os.path.join('images', random_image)
    
    # Отправляем изображение
    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(photo)

def get_wikipedia_info(query: str) -> str:
    """Получает информацию с Wikipedia"""
    try:
        url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем первый содержательный абзац
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 100 and not p.find('sup'):
                return f"{text}\n\n🔗 Подробнее: {url}"
        
        return "Информация найдена, но текст слишком короткий. Читайте полную статью: {url}"
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return "Не удалось получить информацию с Wikipedia."
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Произошла ошибка при обработке запроса."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка сообщений пользователя"""
    user_message = update.message.text.lower()
    response = "Не совсем понял ваш вопрос. Попробуйте задать его иначе."
    
    # Поиск подходящего ответа в базе знаний
    for question, data in KNOWLEDGE_BASE.items():
        if question in user_message:
            if data['custom_answer']:
                response = data['custom_answer']
            else:
                response = get_wikipedia_info(data['source'])
            break
    
    await update.message.reply_text(response)

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(token).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", image_command))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("EcoLev_Bot запущен и готов к работе!")
    application.run_polling()

if __name__ == '__main__':
    main()
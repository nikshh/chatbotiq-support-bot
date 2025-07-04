import telebot
from datetime import datetime

from src.settings import settings
from src.answer_matching import match_answer
from src.models import get_session

bot = telebot.TeleBot(settings.token)
MAX_MESSAGES = 3

def send_business_message(chat_id, text, business_connection_id):
    try:
        bot.send_message(chat_id, text, business_connection_id=business_connection_id)
        print(
            f"Бизнес-сообщение отправлено в чат {chat_id} с Business ID: {business_connection_id}"
        )
    except Exception as e:
        print(f"Ошибка отправки бизнес-сообщения: {e}")


@bot.business_message_handler(func=lambda message: True)
def business_message_handler(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    business_id = message.business_connection_id
    chat_id = message.chat.id
    print(
        f"[{timestamp}] БИЗНЕС-СООБЩЕНИЕ: {message.from_user.username} (Chat ID: {chat_id}, Business ID: {business_id}) -> {message.text}"
    )
    print(f"💡 Business Connection ID для ответа: {business_id}")

    not_found_message = "".join(
        [
            "Извините, я не смог найти точный ответ на ваш вопрос. 🤔\n\n"
            "Для получения персональной помощи обратитесь к нашему оператору - "
            "он сможет помочь вам более детально!\n\n"
            "Напишите /operator для связи с оператором."
        ]
    )

    with get_session() as session:
        best_answer = match_answer(message.text, session)
        if not best_answer:
            send_business_message(chat_id, not_found_message, business_id)
            return 
        
        i = 0
        while best_answer and i < MAX_MESSAGES:
            send_business_message(chat_id, best_answer.text, business_id)
            # print(best_answer.next_answer_id)
            best_answer = best_answer.next_answer
            i += 1
            

if __name__ == "__main__":
    bot.infinity_polling()

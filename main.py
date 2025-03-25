import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image

# Заголовок додатку
st.title("Хмара слів")

# Якщо список слів ще не існує в сесії, створюємо його
if "words" not in st.session_state:
    st.session_state.words = []


# Функція для додавання нового слова в список
def add_word():
    new_word = st.session_state.new_word.strip()  # Отримуємо нове слово і видаляємо зайві пробіли
    if new_word:  # Якщо поле для слова не порожнє
        st.session_state.words.append(new_word) # Додаємо слово в список
    else:
        st.warning("Будь ласка, введіть слово або текст") # Якщо слово порожнє - попередження


# Поле для введення слова користувачем
st.text_area("Введіть слово:", key="new_word", on_change=add_word)

# Кнопка для додавання слова
if st.button("Додати"):
    add_word()

# Якщо список слів не порожній, створюємо хмару слів
if st.session_state.words:
    text = " ".join(st.session_state.words) # Об'єднуємо всі слова в один рядок
    mask = np.array(Image.open("cloud_mask.png").convert("L")) # Завантажуємо маску для хмари слів

    # Створюємо хмару слів з використанням WordCloud
    word_cloud = WordCloud(
        width=1200,
        height=800,
        mode="RGBA",
        background_color=None,
        colormap="gist_ncar", # Вибір кольорової палітри для хмари
        collocations=False, # Вимикаємо спільні комбінації слів
        stopwords=STOPWORDS, # Стандартні стоп-слова
        mask=mask
    ).generate(text) # Генеруємо хмару слів

    # Візуалізація хмари слів
    fig, ax = plt.subplots()
    ax.imshow(word_cloud, interpolation='bilinear') # Відображаємо хмару слів на графіку
    ax.axis("off")  # Вимикаємо осі
    fig.patch.set_alpha(0.0) # Робимо фон прозорим
    st.pyplot(fig) # Відображаємо зображення в Streamlit

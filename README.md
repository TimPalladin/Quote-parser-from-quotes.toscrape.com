# Quotes Parser

Простой, но полноценный парсер цитат с сайта [quotes.toscrape.com](https://quotes.toscrape.com/).

### Возможности
- Собирает **все цитаты** (~100 шт.) со всех страниц сайта
- Пагинация (автоматический переход по страницам)
- Сохранение в `quotes.json`
- Красивый Excel-файл с форматированием (цветные заголовки, автоширина, перенос текста)
- Подсчёт тегов и обработка списков

### Технологии
- Python 3
- requests + BeautifulSoup4
- pandas
- openpyxl

### Скриншоты

<image-card alt="Результат парсинга" src="image.png" ></image-card>

### Возможные улучшения в будущем
- Telegram-бот на основе этого парсера
- Фильтры по автору и тегам
- GUI-интерфейс

### Как запустить

```bash
# 1. Клонируй репозиторий
git clone https://github.com/TimPalladin/Quote-parser.git

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Запусти
python main.py


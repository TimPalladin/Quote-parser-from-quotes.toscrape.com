import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from openpyxl.styles import Font, Alignment
import openpyxl
import json
import time

# Загрузка и сохранение
FILE_NAME='s.json'
def load_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)          # возвращает список словарей
    except:
        return []   # если файла нет — пустой список



def save_data(data):
    with open(FILE_NAME,'w', encoding="utf-8") as jf:
        json.dump(data,jf,indent=4,ensure_ascii=False)

def parse_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Ошибка подключения!')
        return []


    html = response.text
    soup = bs(html, 'html.parser')
    quotes = []


    for block in soup.find_all('div', class_='quote'):
        text_tag = block.find('span', class_='text')
        author_tag = block.find('small', class_='author')
        tags_tags = block.find_all('a', class_='tag')

        text = text_tag.text.strip() if text_tag else ""
        author = author_tag.text.strip() if author_tag else "Unknown"
        tags = [tag.text for tag in tags_tags]

        quotes.append({'quote': text,
                       'author': author,
                       'tags': tags,
                       'tags_count': len(tags)})
    return quotes

def get_next_page(soup):
    next_button = soup.find('li', class_='next')
    if next_button:
        a_tag = next_button.find('a')
        if a_tag:
            return "https://quotes.toscrape.com" + a_tag.get('href')
    else:
        return None

def parse_all_pages(base_url="https://quotes.toscrape.com/"):
    all_quotes = []
    url = base_url
    while url:
        print(f'Парсим страницу: {url}')
        new_quotes = parse_page(url)

        for q in new_quotes:  # Анти-дубль
            if not any(before.get('quote') == q['quote'] for before in all_quotes):
                all_quotes.append(q)

        soup = bs(requests.get(url).text, 'html.parser')
        url = get_next_page(soup)
        time.sleep(1)
    return all_quotes


EXCEL_FILENAME = 'data.xlsx'


def save_to_excel(all_quotes, EXCEL_FILENAME):
    df = pd.DataFrame(all_quotes)
    if 'tags' in df.columns:
        df['tags'] = df['tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
    df = df.rename(columns={
        'quote': 'Цитаты',
        'author':'Авторы',
        'tags': 'Теги',
        'tags_count': 'Количество тегов'

    })

    with pd.ExcelWriter(EXCEL_FILENAME, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Цитаты')



        workbook = writer.book
        worksheet = writer.sheets['Цитаты']

        header_font = Font(bold=True, color='FFFFFF')
        header_alignment = Alignment(horizontal='center')





        for cell in worksheet[1]:
            cell.font = header_font
            cell.alignment = header_alignment
            cell.fill = openpyxl.styles.PatternFill(start_color="366092",
                                                    end_color="366092",
                                                    fill_type="solid")

        # === Автоширина колонок ===
        for column in worksheet.columns:
            column_letter = column[0].column_letter
            max_length = 0
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = min(max_length + 5, 70)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Перенос текста в колонке Цитаты
        for cell in worksheet['A']:  # колонка A = Цитаты
            cell.alignment = Alignment(wrap_text=True, vertical='top')




# url="https://quotes.toscrape.com/"



if __name__=='__main__':

    all_quotes = parse_all_pages()
    save_data(all_quotes)
    save_to_excel(all_quotes, EXCEL_FILENAME)

    print(f'В списке {len(load_data())} цитат.')






    # print('==Первые=5=цитат==')
    # rec=load_data()
    # for number in range(5):
    #     print(f'№{number}.{rec[number-1]["quote"]}\nАвтор: {rec[number-1]["author"]}')









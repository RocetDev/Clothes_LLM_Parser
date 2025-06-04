import parsercode
import openai
import json


def create_parser_object(api_key: str) -> openai.OpenAI: # type: ignore
    return openai.OpenAI(
        api_key=api_key,
        base_url='https://openrouter.ai/api/v1'
    )


def parse_info_textpage(text: str, parser_object: openai.OpenAI, 
               model: str='meta-llama/llama-3.3-8b-instruct:free', temp=0.1, top_p=0.1) -> dict:
    system_prompt = """Ты профессиональный китайский сборщик данных для предприятия, занимающегося анализом цен на маркетплейсах. Твоя задача — из переданного пользователем текста (в формате markdown) извлечь данные о товаре и упаковать их в JSON по строго заданному шаблону.

Важное требование:  
- Выводи **только** JSON-объект, без каких-либо префиксов, суффиксов, заголовков, слов "json", переносов строк вне JSON-формата или других символов.  
- JSON должен быть корректно сформирован: двойные кавычки, правильные типы данных (числа, булевы значения), без лишних отступов и прочего.

Пример правильного вывода:  
{"photo": "https://example.com/image.jpg", "brend": "Название", "characteristics": "...", "price": 1234, "information": "...", "categori": "...", "gender": true}

Отправляй только JSON, ничего больше.

Требования к данным:
1. Фото товара — URL с наилучшим качеством из всех упомянутых. Если ссылка указана только относительная (например, "/upload/iblock/..."), преобразуй её в полный URL, добавив корректный домен сайта, откуда берутся данные. Например:  
   Неправильно: "/upload/resize_cache/iblock/428/500_500_...jpg"  
   Правильно: "https://mirey.su/upload/iblock/428/4wkkp1ujo7g5au1nf0bt0upcc059u2td.jpg"  
   Адрес сайта может меняться, используй исходный домен из ссылки пользователя, если он есть.

2. Бренд товара.

3. Основные характеристики товара.

4. Цена — число (целое или с плавающей точкой).

5. Описание товара — текст.

6. Категории и подкатегории товара.

7. Гендер товара — булево значение:  
   true — если товар для мужчин (например, мужская футболка поло),  
   false — если товар для женщин.

Требования к формату вывода:  
Отправь только JSON-объект строго по шаблону, без лишнего текста, комментариев, пояснений и технических сообщений по типу - <JSON code>.  
Пример правильного JSON:  
{"photo": "<url>", "brend": "<текст>", "characteristics": "<текст>", "price": <число>, "information": "<текст>", "categori": "<текст>", "gender": <true или false>}

Относительно ссылок на изображения — они должны быть рабочими, то есть вести на реальный файл изображения, а не просто путь к директории.

Выполняй работу ответственно и качественно, как настоящий патриот и добросовестный сотрудник, поскольку от результата зависит твоя репутация и работа.
    """
    json_response = None
    try:
        response = parser_object.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Выполни парсинг данных: " + text}
            ],
            temperature=temp,
            top_p=top_p
        )
        
        json_response = response.choices[0].message.content.strip()

        return json.loads(json_response.encode('utf-8'))
    except Exception as e:
        print(f"[EXCEPTION] ERROR when parse Info!!!:\n ERROR MESSAGE>: {e}")
        return {"ERROR": str(e), "TEXT": json_response}


def parse_catolog_textpage(text: str, parser_object: openai.OpenAI, time: bool=True,
                  model: str='meta-llama/llama-3.3-8b-instruct:free', temp=0.1, top_p=0.1) -> dict:
    products = {"products": []}
    product_links = None

    system_prompt = """
Ты профессиональный китайский сборщик данных для предприятия, занимающегося анализом цен на маркетплейсах. Твоя задача — из переданного пользователем текста каталога товаров продавца на маркетплэйсе (в формате markdown) извлечь ссылки на все товары продавца и упаковать их в python list через запятую, где ссылка это текстовый тип данных python.

Важное требование:  
- Выводи **только** python list, без каких-либо префиксов, суффиксов, заголовков, слов "list", переносов строк вне python list или других символов.  
- Python list должен быть корректно сформирован: двойные кавычки, правильные типы данных (числа, булевы значения), без лишних отступов и прочего.

Пример правильного вывода:
["https://www.wildberries.ru/catalog/172262230/detail.aspx", "https://www.wildberries.ru/catalog/173710589/detail.aspx", "https://www.wildberries.ru/catalog/216155901/detail.aspx", "https://www.wildberries.ru/catalog/175975740/detail.aspx"]

Если ссылка указана только относительная (например, "/upload/iblock/..."), преобразуй её в полный URL, добавив корректный домен сайта, откуда берутся данные. Например:  
   Неправильно: "/upload/resize_cache/iblock/428/500_500_...jpg"  
   Правильно: "https://mirey.su/upload/iblock/428/4wkkp1ujo7g5au1nf0bt0upcc059u2td.jpg"  
   Адрес сайта может меняться, используй исходный домен из ссылки пользователя, если он есть.

Ссылки которые не относятся к каталогу продавца в формируемый список добавляться не должны.

Относительно ссылок на изображения — они должны быть рабочими, то есть вести на реальный файл изображения, а не просто путь к директории.

Выполняй работу ответственно и качественно, как настоящий патриот и добросовестный сотрудник, поскольку от результата зависит твоя репутация и работа.
    """

    try:
        response = parser_object.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Выполни парсинг данных: " + text}
            ],
            temperature=temp,
            top_p=top_p
        )
        
        product_links = response.choices[0].message.content.strip()
        product_links = eval(product_links) # convert string representasion of list to real python list
    except Exception as e:
        print(f"ERROR in link parse catalog:\nERROR MESSAGE>: {e}")

    for link in product_links:
        text_page = parsercode.cleaning_html_page(parsercode.scrape(link, time=time))
        product_info = parse_info_textpage(text_page, parser_object, temp=temp, top_p=top_p, model=model)
        products["products"].append(product_info)

    return products



    
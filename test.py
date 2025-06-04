import parsercode
import parserinfo
import json

# URL = 'https://choux.ru/product/polo-iz-hlopka-ping-pong-games-shokoladnoe' # for example
URL = 'https://choux.ru/collection/futbolki-i-topy' # cataloge example


parser_obj = parserinfo.create_parser_object(
    api_key='<YOUR OPENROUTER API KEY>'
)

with open('product_info.json', 'w', encoding='utf-8') as file:
    print('[INFO] Parsing starts')
    page = parsercode.cleaning_html_page(parsercode.scrape(URL, time=False))
    print('[INFO] Parsing ends')

    print("[INFO] Parsing the product from page...")
    # product_info = parserinfo.parse_info(page, parser_obj) # , model='meta-llama/llama-3.3-70b-instruct:free' 'microsoft/phi-4-reasoning-plus:free'
    products = parserinfo.parse_catolog_textpage(page, parser_obj, time=False, model='microsoft/phi-4-reasoning-plus:free')
    json.dump(products, file)

    print('[INFO] File created!')

    print('[INFO-END] Parsing compleate!')


print(json.loads(open('product_info.json').readline()))
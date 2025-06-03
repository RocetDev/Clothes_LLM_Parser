import parsercode
import parserinfo
import json

URL = 'https://choux.ru/product/polo-iz-hlopka-ping-pong-games-shokoladnoe' # for example


parser_obj = parserinfo.create_parser_object(
    api_key='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'
)

with open('product_info.json', 'w', encoding='utf-8') as file:
    print('[INFO] Parsing starts')
    page = parsercode.cleaning_html_page(parsercode.scrape(URL))
    print('[INFO] Parsing ends')

    print("[INFO] Parsing the product from page...")
    product_info = parserinfo.parse_info(page, parser_obj) # , model='meta-llama/llama-3.3-70b-instruct:free'
    json.dump(product_info, file)

    print('[INFO] File created!')

    print('[INFO-END] Parsing compleate!')


print(json.loads(open('product_info.json').readline()))
import re


class SkuUtils:
    @staticmethod
    def __separate_words(text: str):
        separated_word = re.sub(r'([A-Za-z])([A-Z])', r'\1 \2', text)

        return separated_word

    @staticmethod
    def __get_capitalized_letters(text: str):
        separated_text = SkuUtils.__separate_words(text)
        capitalized_text = separated_text.title()

        groups = re.findall(r'\b(\w)', capitalized_text)
        letters = ''.join(groups)

        return letters

    @staticmethod
    def generate_sku(supplier_name: str, product_name: str, category: int):
        supplier_name_letters = SkuUtils.__get_capitalized_letters(supplier_name)
        product_name_letters = SkuUtils.__get_capitalized_letters(product_name)

        return f'{supplier_name_letters}{category}-{product_name_letters}'

from rest_framework import serializers

from .models import Product

import re


class ProductSerializer(serializers.ModelSerializer):

    sku = serializers.CharField(max_length=32, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'category', 'average_review', 'customers', 'supplier']

    @staticmethod
    def __separate_words(text: str):
        separated_word = re.sub(r'([A-Za-z])([A-Z])', r'\1 \2', text)

        return separated_word

    @staticmethod
    def __get_capitalized_letters(text: str):
        separated_text = ProductSerializer.__separate_words(text)
        capitalized_text = separated_text.title()

        groups = re.findall(r'\b(\w)', capitalized_text)
        letters = ''.join(groups)

        return letters

    @staticmethod
    def __generate_sku(supplier_name: str, product_name: str, category: int):
        supplier_name_letters = ProductSerializer.__get_capitalized_letters(supplier_name)
        product_name_letters = ProductSerializer.__get_capitalized_letters(product_name)

        return f'{supplier_name_letters}{category}-{product_name_letters}'

    def create(self, validated_data):
        supplier_name = validated_data.get('supplier').name
        product_name = validated_data.get('name')
        category = validated_data.get('category')

        sku = self.__generate_sku(supplier_name, product_name, category)

        product = Product.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            sku=sku,
            category=validated_data.get('category'),
            supplier=validated_data.get('supplier')
        )

        return product

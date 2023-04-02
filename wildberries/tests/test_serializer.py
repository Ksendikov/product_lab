from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from wildberries.serializer import CardSerializer
from unittest.mock import MagicMock, patch
from wildberries.pydantic import CardPydantic
from wildberries.models import Card


class CardSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            'article': 12345,
            'file': MagicMock(),
        }
        self.serializer = CardSerializer()

    def test_serializer_with_article(self):
        data = {'article': 123456}
        result = self.serializer.validate(data)
        self.assertEqual(result, data)

    def test_serializer_with_file(self):
        file = SimpleUploadedFile("file.xlsx", b"file_content")
        data = {'file': file}
        result = self.serializer.validate(data)
        self.assertEqual(result, data)

    def test_validate_with_both_article_and_file_fields(self):
        serializer = CardSerializer(data={
            'article': self.data['article'],
            'file': self.data['file'],
        })
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            cm.exception.detail,
            {'error_two_field': ['Only one field should be filled in']},
        )

    def test_validate_with_no_article_or_file_fields(self):
        serializer = CardSerializer(data={})

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(
            cm.exception.detail,
            {'error_none_field': ['The field for article or file must be filled in']},
        )

    def test_validate_save_database(self):
        expected_card = CardPydantic(
            id=self.data['article'],
            brand='Brand',
            name='Title',
        )
        page = {'data': {'products': [expected_card.dict(by_alias=True)]}}
        with patch('wildberries.utils.make_request', return_value=page):
            serializer = CardSerializer(data={'article': self.data['article']})
            self.assertTrue(serializer.is_valid())
            serializer.save()
            card = Card.objects.get(article=self.data['article'])
            self.assertEqual(card.article, self.data['article'])
            self.assertEqual(card.brand, expected_card.brand)
            self.assertEqual(card.title, expected_card.title)

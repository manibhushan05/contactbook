from django.test import TestCase
from model_mommy import mommy

from contact.models import ContactBook, Contact


class ContactBookTestModel(TestCase):
    def setUp(self):
        self.instance = mommy.make(ContactBook, make_m2m=True)
        self.instances = mommy.make(ContactBook, make_m2m=True, _quantity=10)

    def test_contact_book_create(self):
        self.assertTrue(isinstance(self.instance, ContactBook))
        self.assertEqual(ContactBook.objects.filter(id=self.instance.id).count(), 1)
        self.assertEqual(ContactBook.objects.count(), 11)


class ContactTestModel(TestCase):
    def setUp(self):
        self.instance = mommy.make(Contact, make_m2m=True)
        self.instances = mommy.make(Contact, make_m2m=True, _quantity=10)

    def test_contact_book_create(self):
        self.assertTrue(isinstance(self.instance, Contact))
        self.assertEqual(Contact.objects.filter(id=self.instance.id).count(), 1)
        self.assertEqual(Contact.objects.count(), 11)

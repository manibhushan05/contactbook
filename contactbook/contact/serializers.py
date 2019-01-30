from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from contact.models import ContactBook, Contact


class ContactBookSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=ContactBook.objects.all())])
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(required=False)
    deleted_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, slug_field="username")
    changed_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    def create(self, validated_data):
        instance = ContactBook.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        ContactBook.objects.filter(id=instance.id).update(**validated_data)
        return ContactBook.objects.get(id=instance.id)


class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=254, required=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(required=False)
    deleted_on = serializers.DateTimeField(allow_null=True, required=False)
    contact_book = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ContactBook.objects.all(),
                                                      required=True)
    created_by = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, slug_field="username")
    changed_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    contact_book_name = serializers.SerializerMethodField()

    @staticmethod
    def get_contact_book_name(instance):
        if isinstance(instance.contact_book, ContactBook):
            return instance.contact_book.name
        return None

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Contact.objects.all(), fields=('contact_book', 'email'))]

    def create(self, validated_data):
        instance = Contact.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        Contact.objects.filter(id=instance.id).update(**validated_data)
        return Contact.objects.get(id=instance.id)

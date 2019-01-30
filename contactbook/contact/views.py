from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics, filters
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from contact.filters import ContactBookFilter
from contact.models import ContactBook, Contact
from contact.search import CustomSearch
from contact.serializers import ContactBookSerializer, ContactSerializer
from contact.utils import success_response, error_response, get_or_none


class ContactBookListView(generics.ListAPIView):
    serializer_class = ContactBookSerializer
    filter_backends = (CustomSearch, filters.OrderingFilter, DjangoFilterBackend)
    filter_class = ContactBookFilter
    ordering_fields = ('-id',)
    search_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        data = {"status": "Success", "status_code": status.HTTP_200_OK, "msg": "Contact Books"}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data["data"] = serializer.data
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data["data"] = serializer.data
        return Response(data)

    def get_queryset(self):
        return ContactBook.objects.order_by('-id')


class ContactBookViewSet(viewsets.ViewSet):
    """
            API for CRUD operation on Contact Book
    """

    def create(self, request):
        """
        :param request:
        :return:
        """
        request.data["created_by"] = self.request.user.username
        request.data["changed_by"] = self.request.user.username
        serializer = ContactBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_201_CREATED, msg='Contact Book is created', data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    def update(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        request.data["changed_by"] = self.request.user.username
        instance = get_or_none(ContactBook, id=pk)
        if not isinstance(instance, ContactBook):
            return error_response(data={"error": "Contact Book does not exist"}, msg='ContactBook does not exists',
                                  status=status.HTTP_404_NOT_FOUND)
        serializer = ContactBookSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_202_ACCEPTED, msg='Contact Book is updated',
                                    data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    def partial_update(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        request.data["changed_by"] = self.request.user.username
        instance = get_or_none(ContactBook, id=pk)
        if not isinstance(instance, ContactBook):
            return error_response(data={"error": "Contact Book does not exist"}, msg='ContactBook does not exists',
                                  status=status.HTTP_404_NOT_FOUND)
        serializer = ContactBookSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_202_ACCEPTED, msg='Contact Book is updated',
                                    data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    @staticmethod
    def retrieve(request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        instance = get_or_none(ContactBook, id=pk)
        if isinstance(instance, ContactBook):
            serializer = ContactBookSerializer(instance=instance)
            return success_response(data=serializer.data, status=status.HTTP_200_OK, msg='success')
        return error_response(data={"error": "Contact Book does not exist"}, msg='ContactBook does not exists',
                              status=status.HTTP_404_NOT_FOUND)

    def soft_delete(self, request, pk):
        contact_book = get_or_none(ContactBook, id=pk)
        if isinstance(contact_book, ContactBook):
            if contact_book.deleted:
                return error_response(status=status.HTTP_400_BAD_REQUEST, msg="Already deleted", data={})
            contact_book.deleted = True
            contact_book.deleted_on = datetime.now()
            contact_book.save()
            contact_book.contacts.update(deleted=True, deleted_on=datetime.now())
            return success_response(
                msg="id: {} deleted successful".format(pk), data={}, status=status.HTTP_202_ACCEPTED)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg="{} does not exists".format(pk), data={})

    def hard_delete(self, request, pk):
        contact_book = get_or_none(ContactBook, id=pk)
        if isinstance(contact_book, ContactBook):
            ContactBook.objects.filter(id=pk).delete()
            print(ContactBook.objects.filter(id=pk))
            return success_response(msg='{} is deleted'.format(pk), status=status.HTTP_202_ACCEPTED, data={})
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg="{} does not exists".format(pk), data={})


class ContactViewSet(viewsets.ViewSet):
    """
            API for CRUD operation on Contact
    """

    def create(self, request):
        """

        :param request:
        :return:
        """
        request.data["created_by"] = self.request.user.username
        request.data["changed_by"] = self.request.user.username
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_201_CREATED, msg='Contact  is created', data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    def update(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        request.data["changed_by"] = self.request.user.username
        instance = get_or_none(Contact, id=pk)
        if not isinstance(instance, Contact):
            return error_response(data={"error": "Contact Book does not exist"}, msg='Contact does not exists',
                                  status=status.HTTP_404_NOT_FOUND)
        serializer = ContactSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_202_ACCEPTED, msg='Contact Book is updated',
                                    data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    def partial_update(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        request.data["changed_by"] = self.request.user.username
        instance = get_or_none(Contact, id=pk)
        if not isinstance(instance, Contact):
            return error_response(data={"error": "Contact Book does not exist"}, msg='Contact does not exists',
                                  status=status.HTTP_404_NOT_FOUND)
        serializer = ContactSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(status=status.HTTP_202_ACCEPTED, msg='Contact Book is updated',
                                    data=serializer.data)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg='Invalid data', data=serializer.errors)

    @staticmethod
    def retrieve(request, pk=None):
        """
        :param request:
        :param pk:
        :return:
        """
        instance = get_or_none(Contact, id=pk)
        if isinstance(instance, Contact):
            serializer = ContactSerializer(instance=instance)
            return success_response(data=serializer.data, status=status.HTTP_200_OK, msg='success')
        return error_response(data={"error": "Contact Book does not exist"}, msg='Contact does not exists',
                              status=status.HTTP_404_NOT_FOUND)

    def soft_delete(self, request, pk):
        contact = get_or_none(Contact, id=pk)
        if isinstance(contact, Contact):
            if contact.deleted:
                return error_response(status=status.HTTP_400_BAD_REQUEST, msg="Already deleted", data={})
            contact.deleted = True
            contact.deleted_on = datetime.now()
            contact.save()
            return success_response(
                msg="id: {} deleted successful".format(pk), data={}, status=status.HTTP_202_ACCEPTED)
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg="{} does not exists".format(pk), data={})

    def hard_delete(self, request, pk):
        contact = get_or_none(Contact, id=pk)
        if isinstance(contact, Contact):
            Contact.objects.filter(id=pk).delete()
            return success_response(msg='{} is deleted'.format(pk), status=status.HTTP_202_ACCEPTED, data={})
        return error_response(status=status.HTTP_400_BAD_REQUEST, msg="{} does not exists".format(pk), data={})


class ContactListView(generics.ListAPIView):
    serializer_class = ContactBookSerializer
    filter_backends = (CustomSearch, filters.OrderingFilter, DjangoFilterBackend)
    filter_class = ContactBookFilter
    ordering_fields = ('-id',)
    search_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: list of contacts
        """
        queryset = self.filter_queryset(self.get_queryset())

        data = {"status": "Success", "status_code": status.HTTP_200_OK, "msg": "Contact Books"}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data["data"] = serializer.data
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data["data"] = serializer.data
        return Response(data)

    def get_queryset(self):
        """

        :return:
        """
        return Contact.objects.all()


class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            response = Response({
                'status': 'success',
                'msg': 'Login Successful',
                'token': token.key,
                'status_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
            return response
        response = Response({
            'status': 'failure',
            'msg': 'Login Unsuccessful',
            'status_code': status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST)
        return response


class UserLogout(APIView):
    @staticmethod
    def delete(self, request, format=None):
        """
        # simply delete the token to force a login
        :param self:
        :param request:
        :param format:
        :return:
        """
        request.user.auth_token.delete()
        return Response({'status': 'success', 'msg': 'Logout Successfull'}, status=status.HTTP_200_OK)

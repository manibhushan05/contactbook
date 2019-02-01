from django.contrib.auth.models import User
from django.db import models


class ContactBook(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    # for audit logs
    created_by = models.ForeignKey(User, null=True, related_name='contact_books_created_by', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, null=True, related_name='contact_books_changed_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # accepts UTF-8
    email = models.EmailField(max_length=254, db_index=True)  # As described in RFC3696 Errata ID 1690
    contact_book = models.ForeignKey(to=ContactBook, on_delete=models.CASCADE, related_name='contacts')

    # for audit logs
    created_by = models.ForeignKey(User, null=True, related_name='contact_created_by', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, null=True, related_name='contact_changed_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        # considering same email in two or more contactbook but unique within contact book
        unique_together = ('contact_book', 'email')

    def __str__(self):
        return self.email

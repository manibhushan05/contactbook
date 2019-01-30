import random
import string

from django.core.exceptions import FieldError
from rest_framework.response import Response


def success_response(status, msg, data, *args, **kwargs):
    response = {
        "status_code": status,
        "status": "success",
        "msg": msg,
        "data": data
    }
    return Response(data=response, status=status)


def error_response(status, msg, data, *args, **kwargs):
    response = {
        "status_code": status,
        "status": "failure",
        "msg": msg,
        "data": data
    }
    return Response(data=response, status=status)


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs, deleted=False)
    except (model.DoesNotExist, ValueError) as err:
        return None
    except model.MultipleObjectsReturned:
        return model.objects.filter(**kwargs).last()
    except TypeError:
        return None
    except FieldError:
        try:
            return model.objects.get(**kwargs)
        except (model.DoesNotExist, ValueError) as err:
            return None
        except model.MultipleObjectsReturned:
            return model.objects.filter(**kwargs).last()
        except TypeError:
            return None


def generate_random_string(N=8):
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))


def create_contact_book():
    from contact.models import ContactBook
    for _ in range(1000000000):
        try:
            ContactBook.objects.create(name=generate_random_string(N=250), created_by_id=2, changed_by_id=2)
        except:
            pass

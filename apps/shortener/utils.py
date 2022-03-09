import uuid


def generate_shortened_code():
    from apps.shortener.models import Shortener

    uid = uuid.uuid4()
    code = uid.hex[:5]

    while Shortener.objects.filter(shortened__exact=code).exists():
        uid = uuid.uuid4()
        code = uid.hex[5:10]

    return code

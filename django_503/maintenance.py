from django_503.models import Config

def is_enabled():
    try:
        return Config.objects.get(key='maintenance').value
    except Config.DoesNotExist:
        return False

def change(value):
    option, created = Config.objects.get_or_create(key='maintenance', defaults={'value': value})
    if option.value != value:
        option.value = value
        option.save()
    return option.value

def enable():
    change(True)

def disable():
    change(False)
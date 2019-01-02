from Employment.models import Employee


def is_valid_key(key):
    try:
        val = int(key)
        return True
    except ValueError:
        return False
    return False

def get_default_employee():
    return Employee.objects.get(user='default')

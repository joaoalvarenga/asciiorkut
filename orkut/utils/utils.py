def check_isdigit_interval(op, interval):
    if op.isdigit():
        return (interval[0] <= int(op) <= interval[1])
    return False


def is_valid_email(email):
    return email.find('@') != -1


def is_valid_gender(gender):
    return len(gender) == 1 and (gender == 'M' or gender == 'F')


def is_valid_birthdate(birthdate):
    flag = False
    if len(birthdate) == 10 and birthdate.count('-') == 2:
        for part in birthdate.split('-'):
            flag = part.isdigit()
        return flag
    return False
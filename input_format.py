import re


def validate_input(user_input):
    if not user_input:
        print("Пустой запрос!\n")
        return False

    if len(re.findall("[0-9!$%&'()*+-/:;<=>?@[\]^_`{|}~]+", user_input)) != 0:
        print("Имя не может содержать цифры или специальные символы!\n")
        return False

    return True


def name_to_list(name):
    return name.replace(",", " ").replace(".", " ").split()


def is_full_name(name):
    return len(name_to_list(name)) == 3


def format_name(name):
    name = name_to_list(name)
    name[1], name[2] = name[1][:1], name[2][:1]
    name = " ".join(name)
    return name

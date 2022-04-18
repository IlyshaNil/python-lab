""" Elib project"""
import requests
import re


def validate(user_input):
    if not user_input:
        print("Пустой запрос!\n")
        return False
     
    if len(re.findall('[0-9]+', user_input)) != 0:
        print("Имя не может содержать цифры!\n")
        return False

    return True


def user_input():
    valid = False
    while not valid:
        employer = input("Введите имя сотрудника:\n")
        valid = validate(employer)
    
    return employer


def is_full_name(name):
    return "." in name or " " in name
    


def main():
    employer = user_input()
    is_full_name(employer)
    print(is_full_name(employer))


if __name__ == '__main__' :
    main()


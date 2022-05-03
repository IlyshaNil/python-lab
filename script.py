""" Elib project"""
import requests
import string
import pprint
import json
from bs4 import BeautifulSoup
from input_format import validate, name_to_list, is_full_name, format_name


def user_input():
    valid = False
    while not valid:
        employer = input("Введите фамилию сотрудника с большой буквы:\n")
        valid = validate(employer)

    return employer


def get_articles(name, full_name=False):
    r = requests.get(
        f"https://elib.bsu.by/browse?type=author&order=ASC&rpp=40&starts_with={name.replace(' ', '+')}"
    )
    soup = BeautifulSoup(r.text, features="html.parser").find_all(
        "li", {"class": "list-group-item"}
    )

    overlap = []
    for tag in soup:
        inner_text = tag.findChildren("a", recursive=False)[0].text
        url = tag.findChildren("a", recursive=False)[0].get("href")
        if name.split()[0] in inner_text or name.split()[0].upper() in inner_text:
            overlap.append(
                [inner_text.replace(",", " ").replace(".", " ").split(), url]
            )

    ditc = {}
    i = 0
    names_map = []
    for name_list in overlap:
        name_list[0][1], name_list[0][2] = name_list[0][1][:1], name_list[0][2][:1]
        name_list[0] = " ".join(name_list[0])
        if not name_list[0] in ditc.keys():
            ditc[name_list[0]] = [name_list[1]]
            if not full_name:
                print(f"{i}. {name_list[0]}")
            i += 1
            names_map.append(name_list[0])
        else:
            ditc[name_list[0]].append(name_list[1])

    if not full_name:
        user_choose = input("\nВыберите номер нужного сотрудника:\n")
        return ditc[names_map[int(user_choose)]]
    else:
        user_choose = name
        return ditc[user_choose]


def main():
    employer = user_input()
    if is_full_name(employer):
        employer = format_name(employer)
        overlap_urls = get_articles(employer, True)
    else:
        overlap_urls = get_articles(name_to_list(employer)[0], False)


if __name__ == "__main__":
    main()

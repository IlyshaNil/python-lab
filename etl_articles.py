import requests
import pprint
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from prettytable import ALL
from input_format import validate_input


def user_input():
    valid = False
    while not valid:
        employer = input("Введите фамилию сотрудника с большой буквы:\n")
        valid = validate_input(employer)

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
    if len(overlap) == 0:
        raise KeyError
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


def create_articles_list(urls_list):
    table = PrettyTable(["Предпросмотр", "Дата выпуска", "Заглавие", "Авторы"])
    table.max_width = 100
    table.hrules = ALL
    for url in urls_list:
        r = requests.get(f'https://elib.bsu.by{url.replace(".", "%2E")}')
        soup = BeautifulSoup(r.text, features="html.parser")
        rows = soup.find("table", attrs={"class": "table"}).find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                table.add_row([ele.text for ele in cols if ele])
    table.sortby = "Дата выпуска"
    print(table)
    return table


def sort_table(table):
    is_sorted = False
    while not is_sorted:
        print("Сортировать таблицу по:\n")
        user_input = {
            1: "Дата выпуска",
            2: "Заглавие",
            3: "Авторы",
            4: "Выйти из программы",
        }
        pprint.pprint(user_input)
        key = int(input())
        if key <= 3:
            table.sortby = user_input[key]
            print(table)
        else:
            is_sorted = True

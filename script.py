from input_format import validate_input, name_to_list, is_full_name, format_name
from etl_articles import user_input, get_articles, create_articles_list, sort_table


def main():
    is_loop = True
    while is_loop:
        try:
            employer = user_input()
            if is_full_name(employer):
                employer = format_name(employer)
                overlap_urls = get_articles(employer, True)
            else:
                overlap_urls = get_articles(name_to_list(employer)[0], False)
            table = create_articles_list(overlap_urls)
            sort_table(table)
            
        except KeyError:
            print("Нет совпадений! Попробуйте еще раз!")
        except IndexError:
            print("Некорректный ввод! Попробуйте еще раз!")
        except ValueError:
            print("Некорректный ввод! Попробуйте еще раз!")
        else:
            is_loop = False


if __name__ == "__main__":
    main()

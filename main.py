from utils import DBManager


def main():
    v = DBManager()
    respons = v.get_hh_data()
    v.create_database('test_hh')
    v.save_data_to_database(respons)
    d = v.get_vacancies_with_keyword('мастер')
    print(d)


if __name__ == '__main__':
    main()

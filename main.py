

from utils import DBManager

def main():

    v = DBManager()
    respons = v.get_hh_data()
    v.create_database('<имя БД>')
    v.save_data_to_database(respons)


if __name__ == '__main__':
    main()

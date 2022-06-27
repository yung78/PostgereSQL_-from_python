import psycopg2


def del_all(pas):
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS phone")
        cur.execute("DROP TABLE IF EXISTS data")
        conn.commit()
        print('Все таблицы далены')
    conn.close()


def create_data_tables(pas):
    print('Создаём структуру БД (таблицы)')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS data"
                    "(id SERIAL PRIMARY KEY,"
                    "name VARCHAR(50) NOT NULL,"
                    "surname VARCHAR(50) NOT NULL,"
                    "email VARCHAR(50));")
        cur.execute("CREATE TABLE IF NOT EXISTS phone"
                    "(id SERIAL PRIMARY KEY,"
                    "data_id INTEGER NOT NULL REFERENCES data(id) ON DELETE CASCADE,"
                    "number BIGINT);")
        conn.commit()
        print('Таблицы базы данных созданы')
    conn.close()


def add_client(pas):
    print('Добавляем нового клиента')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        query_sel1 = "SELECT * FROM data;"
        query_sel2 = "SELECT * FROM phone;"
        data1 = (input('Имя: '), input('Фамилия: '), input('email: '))
        query_in1 = f"INSERT INTO data(name, surname, email) VALUES {data1}"
        cur.execute(query_in1)
        conn.commit()
        cur.execute(query_sel1)
        data2 = (cur.fetchall()[-1][0], input('Номер телефона(только цифры): '))
        if data2[1] == '':
            cur.execute(query_sel1)
            data2 = (cur.fetchall()[-1][0], 0)
        query_in2 = f"INSERT INTO phone(data_id, number) VALUES {data2}"
        cur.execute(query_in2)
        conn.commit()
        cur.execute(query_sel1)
        print(cur.fetchall())
        print()
        cur.execute(query_sel2)
        print(cur.fetchall())
    conn.close()
    print('Клиент добавлен в базу данных')


def add_phone(pas):
    print('Добавляем телефон для существующего клиента')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        ask_data = (input('Имя: '), input('Фамилия: '))
        ask_num = input('Номер телефона(только цифры): ')
        query_sel1 = "SELECT id FROM data WHERE name=%s AND surname=%s;"
        query_sel2 = "SELECT number FROM phone WHERE data_id=%s;"
        query_sel3 = "SELECT * FROM phone;"
        query_upd1 = "UPDATE phone SET number=%s WHERE data_id=%s;"
        cur.execute(query_sel1, ask_data)
        data_id = cur.fetchone()
        cur.execute(query_sel2, data_id)
        data_num = cur.fetchone()
        if data_num[0] == 0:
            cur.execute(query_sel1, ask_data)
            data = (ask_num, cur.fetchone()[0])
            cur.execute(query_upd1, data)
            conn.commit()
        else:
            cur.execute(f"INSERT INTO phone(data_id, number) VALUES ({data_id[0]}, {ask_num});")
            conn.commit()
        cur.execute(query_sel3)
        print(cur.fetchall())
    conn.close()
    print('Телефон добавлен в базу данных')


def change_data(pas):
    print('Изменяем данные о клиенте')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        ask_data = (input('Имя: '), input('Фамилия: '))
        query_sel1 = "SELECT id FROM data WHERE name=%s AND surname=%s;"
        query_sel2 = "SELECT * FROM data;"
        query_sel3 = "SELECT * FROM phone;"
        query_upd1 = "UPDATE data SET name=%s WHERE id=%s;"
        query_upd2 = "UPDATE data SET surname=%s WHERE id=%s;"
        query_upd3 = "UPDATE data SET email=%s WHERE id=%s;"
        query_upd4 = "UPDATE phone SET number=%s WHERE data_id=%s;"
        cur.execute(query_sel1, ask_data)
        data_id = cur.fetchone()
        print('Какие данные Вы хотите изменить:\n'
              '1.Имя\n'
              '2.Фамилия\n'
              '3.email\n'
              '4.Номер телефона\n')
        change_str = input('Введите № пунктов:')
        if '1' in change_str:
            new_name = input('Новое имя: ')
            cur.execute(query_upd1, (new_name, data_id[0]))
            conn.commit()
        if '2' in change_str:
            new_surname = input('Новая фамилия: ')
            cur.execute(query_upd2, (new_surname, data_id[0]))
            conn.commit()
        if '3' in change_str:
            new_email = input('Новый email: ')
            cur.execute(query_upd3, (new_email, data_id[0]))
            conn.commit()
        if '4' in change_str:
            new_number = input('Новый номер телефона: ')
            cur.execute(query_upd4, (new_number, data_id[0]))
            conn.commit()
        cur.execute(query_sel2)
        print(cur.fetchall())
        print()
        cur.execute(query_sel3)
        print(cur.fetchall())
        conn.close()


def del_num(pas):
    print('Удалаляем телефон для существующего клиента')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        ask_data = (input('Имя: '), input('Фамилия: '))
        query_sel1 = "SELECT id FROM data WHERE name=%s AND surname=%s;"
        query_sel2 = "SELECT number FROM phone WHERE data_id=%s;"
        query_sel3 = "SELECT * FROM phone;"
        query_upd1 = "UPDATE phone SET number=%s WHERE data_id=%s;"
        cur.execute(query_sel1, ask_data)
        data_id = cur.fetchone()
        cur.execute(query_sel2, data_id)
        data_num = cur.fetchall()
        if data_num[0][0] == 0:
            print(f'Номер телефона клиента {ask_data[0]} {ask_data[1]} в базе отсутствует.')
            return conn.close()
        if len(data_num) == 1:
            cur.execute(query_upd1, (0, data_id[0]))
            conn.commit()
            cur.execute(query_sel3)
            print('Телефон удалён из базы данных')
            return conn.close()
        else:
            print('Номера телефонов клиента:')
            for num in data_num:
                print(num[0])
            del_n = int(input('Введите номер, который хотите удалить: '))
            if (del_n,) not in data_num:
                print('Вы ошиблись, попробуйте снова')
                del_n = int(input('Введите номер, который хотите удалить: '))
                if (del_n,) not in data_num:
                    print('Вы ошиблись, попробуйте снова')
                    del_n = int(input('Введите номер, который хотите удалить: '))
                    if (del_n,) not in data_num:
                        conn.commit()
                        print('Вы ошиблись, завершение процесса')
                        return conn.close()
            cur.execute("DELETE FROM phone WHERE number=%s;", (del_n,))
            conn.commit()
            cur.execute(query_sel3)
            print(cur.fetchall())
            conn.close()
            print('Телефон удалён из базы данных')


def del_client(pas):
    print('Удалаляем существующего клиента')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM data;")
        print(cur.fetchall())
        print()
        cur.execute("SELECT * FROM phone;")
        print(cur.fetchall())
        ask_data = (input('Имя: '), input('Фамилия: '))
        query_sel1 = "SELECT id FROM data WHERE name=%s AND surname=%s;"
        query_sel2 = "SELECT * FROM data;"
        query_sel3 = "SELECT * FROM phone;"
        query_del1 = "DELETE FROM data WHERE name=%s AND surname=%s;"
        query_del2 = "DELETE FROM phone WHERE number=%s;"
        cur.execute(query_sel1, ask_data)
        data_id = cur.fetchone()
        cur.execute(query_del2, data_id)
        conn.commit()
        cur.execute(query_del1, ask_data)
        conn.commit()
        cur.execute(query_sel2)
        print(cur.fetchall())
        print()
        cur.execute(query_sel3)
        print(cur.fetchall())
        conn.close()


def find_client(pas):
    print('Ищем клиента по его данным (имени, фамилии, email-у или телефону')
    conn = psycopg2.connect(database='Homework2', user='postgres', password=pas)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM data;")
        print(cur.fetchall())
        print()
        cur.execute("SELECT * FROM phone;")
        print(cur.fetchall())
        query_sel1 = "SELECT data_id FROM phone WHERE number=%s;"
        query_sel2 = "SELECT id FROM data WHERE name=%s AND surname=%s;"
        query_sel3 = "SELECT id FROM data WHERE email=%s;"
        query_sel4 = f"SELECT * FROM data WHERE id=%s;"
        query_sel5 = "SELECT * FROM phone WHERE data_id=%s;"
        print('По каким данным осуществляется поиск:\n'
              '1.Имя\n'
              '2.Фамилия\n'
              '3.email\n'
              '4.Номер телефона\n')
        ask_data = input('Введите № пунктов:')
        ask_list = []
        if '1' in ask_data:
            ask_list += ['name']
        if '2' in ask_data:
            ask_list += ['surname']
        if '3' in ask_data:
            ask_list += ['email']
        if '4' in ask_data:
            ask_list += ['number']
        if 'number' in ask_list:
            print('Номера телефона будет достаточно.')
            ask_num = input('Введите номер телефона: ')
            cur.execute(query_sel1, (ask_num,))
            ask_id = cur.fetchone()
            cur.execute(query_sel4, ask_id)
            print(cur.fetchone())
            cur.execute(query_sel5, ask_id)
            print(cur.fetchone())
            return conn.close()
        if 'email' in ask_list:
            print('Адреса электронной почты будет достаточно.')
            ask_mail = input('Введите email: ')
            cur.execute(query_sel3, (ask_mail,))
            ask_id = cur.fetchone()
            cur.execute(query_sel4, ask_id)
            print(cur.fetchone())
            cur.execute(query_sel5, ask_id)
            print(cur.fetchone())
            return conn.close()
        if 'name' in ask_list:
            print('Имени будет не достаточно.')
            ask_data = (input('Имя: '), input('Фамилия: '))
            cur.execute(query_sel2, ask_data)
            ask_id = cur.fetchone()
            cur.execute(query_sel4, ask_id)
            print(cur.fetchone())
            cur.execute(query_sel5, ask_id)
            print(cur.fetchone())
            return conn.close()
        if 'surname' in ask_list:
            print('Фамилии будет не достаточно.')
            ask_data = (input('Имя: '), input('Фамилия: '))
            cur.execute(query_sel2, ask_data)
            ask_id = cur.fetchone()
            cur.execute(query_sel4, ask_id)
            print(cur.fetchone())
            cur.execute(query_sel5, ask_id)
            print(cur.fetchone())
            return conn.close()


def start_all():
    pas = input('Введите пароль для работы сбазой данных postgreSQL: ')
    create_data_tables(pas)  # 1. Функция, создающая структуру БД (таблицы)
    add_client(pas)  # 2. Функция, позволяющая добавить нового клиента
    add_phone(pas)  # 3. Функция, позволяющая добавить телефон для существующего клиента
    change_data(pas)  # 4. Функция, позволяющая изменить данные о клиенте
    del_num(pas)  # 5. Функция, позволяющая удалить телефон для существующего клиента
    del_client(pas)  # 6. Функция, позволяющая удалить существующего клиента
    find_client(pas)  # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    # del_all(pas)  # Удаляет все таблицы


start_all()

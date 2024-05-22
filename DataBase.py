import sqlite3
import config
import logging

print(1)
class Data:
    def __init__(self):
        self.db_way = config.db_way
        self.db_name = config.db_name

    def execute_request(self, execute: str, return_value: bool = False, parametrs: list = None):
        con = sqlite3.connect(self.db_way)
        cur = con.cursor()
        try:
            if return_value:
                value = cur.execute(execute).fetchall()
            elif parametrs:
                cur.execute(execute, tuple(parametrs))
            else:
                cur.execute(execute)
        except sqlite3.Error as error:
            logging.warning("Ошибка при работе с SQLite", error)
        con.commit()
        con.close()
        if return_value:
            return value

    def insert_row(self, name_column: list, value_column: list):
        names = ''
        values = ''
        for i in range(0, len(name_column) - 1):
            names += name_column[i] + ','
            values += '?,'
        names+=name_column[-1]
        values+='?'
        execute = f'''INSERT INTO {self.db_name} ({names}) VALUES ({values})'''
        try:
            Data().execute_request(execute=execute, parametrs=value_column)
        except sqlite3.Error as error:
            logging.warning("Ошибка при работе с SQLite", error)

    def select_from_table(self, select_column: list, elements_conditions: list, elements_values: list):
        execute = ''
        selects = ''
        condition = ''
        for i in range(0, len(select_column) - 1):
            selects += select_column[i] + ','
        selects += select_column[-1]
        for i in range(0, len(elements_conditions) - 1):
            condition += elements_conditions[i] + '=' + elements_values[i] + ','
        condition += elements_conditions[-1] + '=' + elements_values[-1]
        execute = f'SELECT {selects} FROM {self.db_name} WHERE {condition}'
        try:
            result=Data().execute_request(execute=execute, return_value=True)
            print(result)
            if result is None:
                return 0
            try:
                result=result[0][0]
            except:
                return 0
            return result
        except sqlite3.Error as error:
            logging.warning("Ошибка при работе с SQLite", error)

    def update_in_table(self, changeable_columns: list, value_column: list,elements_conditions: list = None, elements_values: list = None):
        execute=''
        changing_columns=''
        condition = ''
        for i in range(0, len(changeable_columns)-1):
            changing_columns+= changeable_columns[i]+'='+'?'+','
        changing_columns += changeable_columns[-1] + '=' + '?'
        if elements_conditions is not None:
            for i in range(0, len(elements_conditions)-1):
                condition+=elements_conditions[i]+'='+'?'+' AND '
                print(condition)
            condition+= elements_conditions[-1]+'='+'?'
            execute=f'UPDATE {self.db_name} SET {changing_columns} WHERE {condition};'
            print(execute)
            Data().execute_request(execute=execute, parametrs=value_column + elements_values)
        else:
            execute = f'UPDATE {self.db_name} SET {changing_columns};'
            Data().execute_request(execute=execute, parametrs=value_column)


    def create_table(self, name_column: list, type_column: list):
        execute = ''
        for i in range(0, len(name_column) - 1):
            execute += name_column[i] + ' ' + type_column[i] + ','
        execute += name_column[-1] + ' ' + type_column[-1]
        execute = f'CREATE TABLE IF NOT EXISTS {self.db_name}({execute});'
        try:
            Data().execute_request(execute=execute)
        except sqlite3.Error as error:
            logging.warning("Ошибка при работе с SQLite", error)

    def is_limit_users(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        result = cursor.execute('SELECT DISTINCT user_id FROM users_data;')
        count = 0
        for i in result:
            count += 1
        connection.close()
        return count >= config.MAX_USERS


Data().create_table(['id', 'user_id', 'user_name', 'user_role', 'tokens', 'request', 'task'],
                        ['INTEGER PRIMARY KEY', 'INTEGER', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])


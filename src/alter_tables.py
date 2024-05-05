import sqlite3
from sqlite3 import OperationalError
from config import get_params, get_car_brands, DBTableName
from main import generate_db_name

def add_datetime_column_and_update_records(db_file, table_names):
    """Добавляет столбец insert_time к заданным таблицам и обновляет все записи, установив текущее время.

    Args:
    db_file (str): путь к файлу базы данных.
    table_names (list): список названий таблиц для добавления столбца и обновления записей.
    """
    # Подключаемся к базе данных
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    for table_name in table_names:
        try:
            # Добавляем столбец insert_time, если он еще не существует
            cursor.execute(f'''
            ALTER TABLE {table_name}
            ADD COLUMN insert_time DATETIME
            ''')
            print(f"Столбец 'insert_time' успешно добавлен в таблицу '{table_name}'.")
        except OperationalError as e:
            print(f"Ошибка при добавлении столбца в таблицу {table_name}: {e}")

        # Обновляем все записи, установив текущее время
        try:
            cursor.execute(f'''
            UPDATE {table_name}
            SET insert_time = (datetime('now', 'localtime'))
            WHERE insert_time IS NULL
            ''')
            updated_rows = cursor.rowcount
            print(f"Обновлено {updated_rows} записей в таблице '{table_name}' с установкой времени вставки.")
        except OperationalError as e:
            print(f"Ошибка при обновлении записей в таблице {table_name}: {e}")

    # Сохраняем изменения и закрываем соединение с базой данных
    connection.commit()
    connection.close()


if __name__ == "__main__":
    params = get_params(brand="")
    for car_brand in get_car_brands():
        params['brand'] = car_brand[1].split(":")[-1]
        db_name = generate_db_name(params)
        # Пример использования функции
        add_datetime_column_and_update_records(db_name, [DBTableName.sold_cars_table_name, DBTableName.cars_table_name])

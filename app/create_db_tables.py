import argparse
import os
import sqlite3
from db_tables import table_names_to_sql

# usage:
# python create_db_tables.py --drop_tables --db_name=sqlite.db


def parse_cmd_line_args_and_create_tables():
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop_tables', action='store_true')
    parser.add_argument('--db_name',     default=os.environ.get('DB_NAME'))

    opts = parser.parse_args()

    print 'using db name: ' + opts.db_name

    connection = sqlite3.connect(opts.db_name)
    cursor = connection.cursor()

    for table_name in table_names_to_sql:
        if opts.drop_tables:
            sql = 'drop table if exists {}'.format(table_name)
            print 'Executing: {}'.format(sql)
            cursor.execute(sql)

        sql = table_names_to_sql[table_name]
        print 'Executing: {}'.format(sql)
        cursor.execute(sql)

    connection.commit()


parse_cmd_line_args_and_create_tables()

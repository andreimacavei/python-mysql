#!/usr/bin/python

import MySQLdb
import argparse
from _mysql_exceptions import OperationalError
from datetime import datetime


def create_connection(host="localhost", user="kheops", passwd="neoman", db="example"):
    return MySQLdb.connect(host, user, passwd, db)

def create_table(db, table_name="testdb"):
    sql = """CREATE TABLE `{0}` (
             `id` int(11) NOT NULL AUTO_INCREMENT,
             `name` char(100) NOT NULL,
             `telephone` char(10) NOT NULL,
             `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
             PRIMARY KEY (`id`)
             ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8""".format(table_name)
    with db:

        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        cursor.execute(sql)

# Unused
def drop_table(db, table_name="testdb"):
    sql = "drop table {}".format(table_name)
    with db:
        cursor = db.cursor()
        cursor.execute(sql)

def show_table(db, table_name="testdb"):
    sql = "SELECT * FROM {}".format(table_name)
    with db:
        cursor = db.cursor()
        cursor.execute(sql)

        results = cursor.fetchall()
        print "%3s %15s %15s %25s" % ('id', 'name', 'telephone', 'date')
        for row in results:
            print "%3i %15s %15s %25s" % (row[0], row[1], row[2], row[3])

def insert_record(db, name, phone, table_name="testdb", record_id = ''):

    if record_id:
        sql = "INSERT INTO {0}(id, name, telephone) values({1},'{2}','{3}')".format(table_name, record_id,
                                                                                name, phone)
    else:
        sql = "INSERT INTO {0}(name, telephone) values('{1}','{2}')".format(table_name, name, phone)

    with db:
        cursor = db.cursor()
        cursor.execute(sql)
        print "Record with id = %d inserted" % cursor.lastrowid

def update_record(db, record_id, name, phone, table_name="testdb"):
    sql = "UPDATE {0} \
           SET name='{1}', telephone='{2}' \
           WHERE id={3}".format(table_name, name, phone, record_id)

    with db:
        cursor = db.cursor()
        cursor.execute(sql)
        print "Record with id = %d updated" % (int(record_id),)

def delete_record(db, record_ids, table_name="testdb"):

    if len(record_ids) == 1 :
        sql = "DELETE FROM {0} WHERE id = {1}".format(table_name, *record_ids)
    elif len(record_ids) == 2 :
        sql = "DELETE FROM {0} WHERE id BETWEEN {1} and {2}".format(table_name, record_ids[0], record_ids[1])
    else :
        record_ids = tuple(record_ids)
        sql = "DELETE FROM {0} WHERE id IN {1}".format(table_name, record_ids)

    with db:
        cursor = db.cursor()
        cursor.execute(sql)
        print "Record(s) deleted"

def get_record(db, record_ids, table_name="testdb"):

    if len(record_ids) == 1:
        sql = "SELECT * FROM {0} WHERE id = {1}".format(table_name, *record_ids)
    elif len(record_ids) == 2:
        sql = "SELECT * FROM {0} WHERE id BETWEEN {1} AND {2}".format(table_name, record_ids[0], record_ids[1])
    else:
        record_ids = tuple(record_ids)
        sql = "SELECT * FROM {0} WHERE id IN {1}".format(table_name, record_ids)

    with db:
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        print "%3s %15s %15s %25s" % ('id', 'name', 'telephone', 'date')
        for row in results:
            print "%3i %15s %15s %25s" % (row[0], row[1], row[2], row[3])

    return results

class valid_telephone(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        try:
            float(values)
        except ValueError:
            raise argparse.ArgumentTypeError("{} is not a valid telephone number".format(values))
        else:
            if len(str(values)) != 10:
                raise argparse.ArgumentTypeError("telephone must have 10 digits")
            setattr(namespace, self.dest, values)


if __name__ == "__main__":

    db = create_connection()

    parser = argparse.ArgumentParser(description='A wrapper in python for MySQLdb API')
#    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-n', '--name', default='')
    parser.add_argument('-p', '--phone', action=valid_telephone)
    parser.add_argument('-i', '--id', default='')
    parser.add_argument('-w', '--with_create', action="store_true")
    parser.add_argument('-s', '--showtable', action="store_true")
    parser.add_argument('-d', '--delrecord', nargs='+')
    parser.add_argument('-u', '--update_record', default='')
    parser.add_argument('-g', '--get_record', nargs='+')
    args = parser.parse_args()

    if args.update_record :
        update_record(db, args.update_record, args.name, args.phone)
        quit()

    if args.with_create :
        create_table(db)

    if args.delrecord :
        delete_record(db, args.delrecord)
        quit()

    if args.get_record :
        get_record(db, args.get_record)
        quit()

    if args.showtable :
        show_table(db)
        quit()


    if not args.name :
        print "name is required"
        quit()

    insert_record(db, args.name, args.phone, record_id=args.id)

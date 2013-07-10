#!/usr/bin/python

import MySQLdb
import argparse
from _mysql_exceptions import OperationalError
from datetime import datetime

db = MySQLdb.connect(host="localhost", user="kheops", passwd="kheops", db="example")
cursor = db.cursor()

def create_table():
    sql = """CREATE TABLE `details` (
             `id` int(11) NOT NULL AUTO_INCREMENT,
             `name` char(100) NOT NULL,
             `telephone` char(10) NOT NULL,
             `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
             PRIMARY KEY (`id`)
             ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    db.commit()

def drop_table():
    sql = "drop table details"
    try:
        cursor.execute(sql)
    except OperationalError :
        pass
    else:
        db.commit()


def insert_record(name, phone):
    sql = "INSERT INTO details(name, telephone) values ('{0}','{1}')".format(name, phone)
    cursor.execute(sql)
    db.commit()

def update_data(name, phone):
    if name and phone:
        sql = "SELECT * FROM details WHERE name='{}' AND telephone='{}'".format(name, phone)
    elif name:
        sql = "SELECT * FROM details WHERE name='{}'".format(name)
    elif phone:
        sql = "SELECT * FROM details WHERE telephone='{}'".format(phone)
    else:
        exit(0)
    print sql

    cursor.execute(sql)
    results = cursor.fetchall()
    print results
    for row in results:
        print row

    sql = "UPDATE details SET %s=%s WHERE %s='%s'"

def show_table():
    sql = "SELECT * FROM details"
    cursor.execute(sql)
    results = cursor.fetchall()
    print "%3s %15s %15s %25s" % ('id', 'name', 'telephone', 'date')
    for row in results:
        print "%3i %15s %15s %25s" % (row[0], row[1], row[2], row[3])

def delete_row(name):
    sql = "DELETE FROM details WHERE name = '{0}'".format(name)
    cursor.execute(sql)
    db.commit()

class valid_date(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            date = datetime.strptime(values, '%Y-%m-%d')
        except ValueError:
            raise argparse.ArgumentTypeError("{0} is not a valid date".format(values))
        else:
            setattr(namespace, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group() 

    parser.add_argument('-n', '--name', default='')
    parser.add_argument('-p', '--phone', default='')
#    parser.add_argument('--date', action=valid_date)
    parser.add_argument('-w', '--withcreate', action="store_true")
    parser.add_argument('-s', '--showtable', action="store_true")
    parser.add_argument('-d', '--delrow', default='')
    parser.add_argument('-u', '--update', default='')
    args = parser.parse_args()

    if args.withcreate :
        drop_table()
        create_table()

    if args.delrow :
        delete_row(args.delrow)
        quit() 

    if args.showtable :
        show_table()
        quit()

    if args.update :
        update_data(args.name, args.phone)
        quit()

    if not args.name :
        print "name is required"
        quit()

    insert_record(args.name, args.phone)
    print "Done"

    cursor.close()

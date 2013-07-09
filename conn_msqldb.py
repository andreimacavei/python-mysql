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
             `telephone` char(50) NOT NULL,
             `date` date NOT NULL,
             PRIMARY KEY (`id`)
             ) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8"""
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


def insert_record(name, phone, date):
    sql = "INSERT INTO details(name, telephone, date) values ('{0}','{1}', '{2}')".format(name, phone, date)
    cursor.execute(sql)
    db.commit()

def show_table():
    sql = "SELECT * FROM details"
    cursor.execute(sql)
    results = cursor.fetchall()
    print "%3s %15s %15s %15s" % ('id', 'name', 'telephone', 'date')
    for row in results:
        print "%3i %15s %15s %15s" % (row[0], row[1], row[2], row[3])

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

    parser.add_argument('--name', default='')
    parser.add_argument('--phone', default='')
    parser.add_argument('--date', action=valid_date)
    parser.add_argument('--addtable', default='')
    parser.add_argument('--showtable', default='')
    parser.add_argument('--delrow', default='')
    args = parser.parse_args()

    if args.addtable :
        drop_table()
        create_table()

    if args.delrow :
        delete_row(args.delrow)
        quit() 

    if args.showtable :
        show_table()
        quit()

    insert_record(args.name, args.phone, args.date)
    print "Done"

    cursor.close()

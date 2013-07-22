import unittest
import sqlite3
from conn_msqldb import *

class TestMySQLdbConnFunctions(unittest.TestCase):

    def setUp(self):
        db  = sqlite3.connect('example.db')
        self.curs = db.cursor()
        self.test_table = 'testdb'

        # Create table
        """self.curs.execute('''CREATE TABLE testdb (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     telephone TEXT,
                     date DATETIME DEFAULT CURRENT_TIMESTAMP
                     )''')"""
    def tearDown(self):
        self.curs.close()    

    def test_insert_record(self):

        # define input
        name = 'Andrei'
        telephone = '0737037718'
        
        # test success
        insert_record(name, telephone, self.test_table)
        last_id = self.curs.lastrowid

        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        assertEqual(row[0], last_id)

        # test failure (should raise _mysql_exceptions.IntegrityError: 1062)
        with self.assertRaises(IntegrityError) as err:
            insert_record(name, telephone, self.test_table, last_id)
        
        excep = err.exception
        self.assertEqual(excep.error_code, 1062)


    def test_update_record(self):
       
        # define input
        insert_record('Andrei', '0723474474', self.test_table)
        last_id = self.curs.lastrowid

        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record = ''.join([str(field) for field in row[:3]])

        # test success
        update_record(last_id, 'Andrei', '0723474474', self.test_table)
        
        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record_same = ''.join([str(field) for field in row[:3]])

        assertEqual(record, record_same)

        update_record(last_id, 'Andrei', '0737037718', self.test_table)
        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record_updated = ''.join([str(field) for field in row[:3]])

        assertFalse(record, record_updated)

    def test_get_record(self)
        
        # define input
        insert_record('Andrei', '0737037718', self.test_table, 5)
        last_record_inserted = get_record(5, self.test_table)

        # test success        
        assertTrue(last_record_inserted)

    def test_delete_record_one(self)

        # define input
        insert_record('Andrei', '0723474474', self.test_table, 11)
        insert_record('Gabriel', '0737037718', self.test_table, 22)

        delete_record(11, self.test_table)

        # test that record was deleted
        record = get_record(11, self.test_table)
        assertFalse(record)

        # test raise error

    def test_delete_record_many(self)

        # define input
        insert_record('Andrei', '0723474474', self.test_table, 11)
        insert_record('Gabriel', '0737037718', self.test_table, 22)
        insert_record('Macavei', '0721400864', self.test_table, 33)



if __name__ == '__main__':
    unittest.main()

#suite = unittest.TestLoader().loadTestsFromTestCase(TestMySQLdbConnFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)


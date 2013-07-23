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
        telephone = '0123456789'
        
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
        insert_record('Andrei', '0123456789', self.test_table)
        last_id = self.curs.lastrowid

        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record = ''.join([str(field) for field in row[:3]])

        # test success
        update_record(last_id, 'Andrei', '0123456789', self.test_table)
        
        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record_same = ''.join([str(field) for field in row[:3]])

        assertEqual(record, record_same)

        update_record(last_id, 'Andrei', '9876543210', self.test_table)
        self.curs.execute('SELECT * FROM %s ORDER BY date DESC' % (self.test_table,))
        row = self.curs.fetchone()
        record_updated = ''.join([str(field) for field in row[:3]])

        assertFalse(record, record_updated)

    def test_get_one_record(self):
        
        # define input
        record_ids = [5]
        insert_record('Andrei', '0123456789', self.test_table, 5)
        last_record_inserted = get_record(record_ids, self.test_table)

        # test success        
        assertTrue(last_record_inserted)

    def test_get_many_records(self):

        records_in = []
        records_out = []
        records_ids = []

        # define input
        insert_record('Ana', '1234509876', self.test_table, 3)
        insert_record('Irina', '0987612345', self.test_table,4)
        insert_record('Suzana', '5432167890', self.test_table,5)

        records_in.append('3Ana1234509876')
        records_out.append('4Irina0987612345')
        records_ids = [3, 4]
        
        # test success 

        results = get_record(records_ids, self.test_table)
        for row in results:
            records_out.append(''.join([str(field) for field in row[:3]]))

        assertEqual(sorted(records_in), sorted(records_out))

    def test_delete_one_record(self):

        # define input
        record_ids = []
        insert_record('Andrei', '0123456789', self.test_table, 11)
        insert_record('Gabriel', '9876543210', self.test_table, 22)

        record_ids = [11]
        delete_record(record_ids, self.test_table)

        # test that record was deleted
        record = get_record(record_ids, self.test_table)
        assertFalse(record)

        # test raise error

    def test_delete_many_records(self):

        # define input
        record_ids = []
        insert_record('Andrei', '0123456789', self.test_table, 11)
        insert_record('Gabriel', '9876543210', self.test_table, 22)
        insert_record('George', '5432106789', self.test_table, 33)

        record_ids = [11, 33]
        delete_record(record_ids, self.test_table)

        # test that two records were deleted
        records = get_record(record_ids, self.test_table)
        assertFalse(records)


if __name__ == '__main__':
    unittest.main()

#suite = unittest.TestLoader().loadTestsFromTestCase(TestMySQLdbConnFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)


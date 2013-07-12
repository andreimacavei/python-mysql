import unittest
import sqlite3
from conn_msqldb import *

class TestMySQLdbConnFunctions(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(':memory:')
        self.curs = conn.cursor()
        
        # Create table
        self.curs.execute('''CREATE TABLE test (
                     id INTEGER AUTO_INCREMENT,
                     name text,
                     telephone text,
                     date text
                     )''')

    def tearDown(self):
        self.curs.close()    

    def test_that_a_record_was_inserted(self):
        # define input
        name = 'Andrei'
        telephone = '0737037718'
        date = datetime.now()
        pre_record_id = self.curs.execute('select last_insert_rowid()')
        
        # apply transformation
        insert_record(name, telephone)

        record_id = self.curs.execute('select last_insert_rowid()')
        result_row = self.curs.execute('select * from test order by rowid desc limit 1')
        row = self.curs.fetchone()
       
        # assert

unittest.main()
#suite = unittest.TestLoader().loadTestsFromTestCase(TestMySQLdbConnFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)


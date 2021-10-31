import configparser
import logging, logging.config
import os
import time
import pandas as pd
import psycopg2
from psycopg2 import pool

class Base:
    def __init__(self):
        self.filename = os.path.basename(__file__)
        self.filename_no_ext = os.path.splitext(self.filename)[0]
        self.ini_filename = self.filename_no_ext + '.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_filename)
        logging.config.fileConfig(self.ini_filename)
        self.logger = logging.getLogger('')
        self.pg_pool = psycopg2.pool.SimpleConnectionPool(1, 2, user=self.config["pg"]["user"],
                                                     password=self.config["pg"]["password"],
                                                     host=self.config["pg"]["host"],
                                                     port=self.config["pg"]["port"],
                                                     database=self.config["pg"]["database"])

    def pg_get_conn_from_pool(self):
        return self.pg_pool.getconn()

    def pg_sqlalchemy_create_conn(self, section):
        self.sqlalchemyconn = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            self.config[section]['user'],
            self.config[section]['password'],
            self.config[section]['host'],
            self.config[section]['database']
        )

    def pg_create_cursor(self, conn):
        cur = conn.cursor()
        self.logger.info("psql cursor created")
        return cur

    def pg_close_cursor(self, cur):
        cur.close()
        self.logger.info("psql cursor closed")

    def pg_execute_dml(self, conn, req):
        cur = self.pg_create_cursor(conn)
        cur.execute(req)
        self.logger.info("psql statement executed:{}".format(req))
        conn.commit()
        self.logger.info("psql statement committed")
        self.pg_close_cursor(cur)

    def pg_execute_select(self, conn, req):
        cur = self.pg_create_cursor(conn)
        cur.execute(req)
        self.logger.info("psql statement executed:{}".format(req))
        res = cur.fetchone()
        self.logger.info("psql statement response:{}".format(res))
        self.pg_close_cursor(cur)

    def pg_release_conn(self, conn):
        # Use this method to release the connection object and send back to connection pool
        self.pg_pool.putconn(conn)
        self.logger.info("Release the current PostgreSQL pool connection")

    def pg_close_all_conn(self):
        #closing database connection.
        # use closeall() method to close all the active connection if you want to turn of the application
        if self.pg_pool:
            self.pg_pool.closeall
        self.logger.info("PostgreSQL connection pool is closed")

    def pg_load_data_to_table_copy(self, conn, filename, delimiter):
        start_time = time.time()
        filepath = os.path.abspath(os.getcwd())
        stmt = "COPY asset_tag_data FROM '" + filepath + "\\" + filename + "' DELIMITER '" + delimiter + "' CSV HEADER"
        self.pg_execute_dml(conn, stmt)
        self.logger.info("DML execution time using postgres copy command: {} seconds".format(time.time() - start_time))

    def pg_load_data_to_table_pandas(self, filename, delimiter):
        start_time = time.time()
        filepath = os.path.abspath(os.getcwd())
        file_name_with_path = filepath+"\\"+ filename
        df = pd.read_csv(file_name_with_path, sep = delimiter)
        self.pg_sqlalchemy_create_conn("pg")
        df.to_sql(
            'asset_tag_data',
            con=self.sqlalchemyconn,
            index=False,
            if_exists='append'
        )
        self.logger.info("DML execution time using pandas and sqlalchemy conn: {} seconds".format(time.time() - start_time))

    def pg_load_data_to_table_copyfrom(self, conn, filename, delimiter):
        start_time = time.time()
        filepath = os.path.abspath(os.getcwd())
        file_name_with_path = filepath+"\\"+ filename
        cur = self.pg_create_cursor(conn)
        file = open(file_name_with_path, 'r')
        next(file)  # Skip the header row.
        cur.copy_from(file, 'asset_tag_data', sep=delimiter)
        conn.commit()
        self.pg_close_cursor(cur)
        self.logger.info("DML execution time using copy from: {} seconds".format(time.time() - start_time))

    @staticmethod
    def get_file_name_details(file_name):
        filename_no_ext = os.path.splitext(file_name)[0]
        ini_filename = filename_no_ext + '.ini'
        return ini_filename


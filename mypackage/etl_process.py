from base import Base
import configparser
import os

class Etl_Process(Base):
    def __init__(self):
        super().__init__()
        file_name = os.path.basename(__file__)
        ini_filename = super().get_file_name_details(file_name)
        self.curr_config = configparser.ConfigParser()
        self.curr_config.read(ini_filename)

if __name__ == '__main__':
    etl = Etl_Process()
    conn1 = etl.pg_get_conn_from_pool()
    #etl.pg_load_data_to_table_copy("asset_tag_data_01_01_21.log", '|')
    #etl.pg_load_data_to_table_pandas("asset_tag_data_01_01_21.log", '|')
    etl.pg_load_data_to_table_copyfrom(conn1,"asset_tag_data_01_01_21.log", '|')
    conn2 = etl.pg_get_conn_from_pool()
    etl.pg_load_data_to_table_copyfrom(conn2, "asset_tag_data_01_01_21.log", '|')
    conn3 = etl.pg_get_conn_from_pool()
    etl.pg_load_data_to_table_copyfrom(conn3, "asset_tag_data_01_01_21.log", '|')
    etl.pg_release_conn(conn1)
    etl.pg_release_conn(conn2)
    etl.pg_release_conn(conn3)
    etl.pg_close_all_conn()

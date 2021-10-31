from base import Base
import datetime
import random
import os
import configparser

class Generate_Data(Base):
    assets = []
    tags = []

    def __init__(self):
        super().__init__()
        self.filename = os.path.basename(__file__)
        filename_no_ext = os.path.splitext(self.filename)[0]
        ini_filename = filename_no_ext + '.ini'
        self.curr_config = configparser.ConfigParser()
        self.curr_config.read(ini_filename)
        self.start_date = datetime.datetime.strptime(self.curr_config["data_settings"]["start_date"], '%Y:%m:%d %H:%M:%S')
        self.time_delta = datetime.timedelta(minutes=int(self.curr_config["data_settings"]["time_delta"]))
        self.time_lapse = datetime.timedelta(days=int(self.curr_config["data_settings"]["time_lapse"]))
        self.asset_count = int(self.curr_config["data_settings"]["asset_count"])
        self.tag_count = int(self.curr_config["data_settings"]["tag_count"])
        data_log_filename = self.curr_config["data_settings"]["data_log_filename"]
        self.curr_log_filename = data_log_filename + self.start_date.strftime("%d_%m_%y")+".txt"
        self.delimiter = self.curr_config["data_settings"]["delimiter"]

    def config_assets(self):
        for i in range(self.asset_count) :
            self.assets.append(100000000+i+1)

    def config_tags(self):
        for i in range(self.tag_count):
            self.tags.append(3000+i+1)

    def generate_data(self):
        itr_time = self.start_date
        end_time = self.start_date + self.time_lapse
        log_file = open(self.curr_log_filename,"w")
        log_file.write("Timestamp{}AssetID{}TagID{}TagValue\n".format(self.delimiter,self.delimiter,self.delimiter))
        for asset_id in self.assets :
            self.logger.info("Data generated for Asset ID: {}".format(asset_id))
            while(itr_time < end_time):
                for tag_id in self.tags :
                    log_file.write("{}{}{}{}{}{}{}\n".format(itr_time,self.delimiter,asset_id,self.delimiter,tag_id,self.delimiter,round(random.uniform(0, 100), 2)))
                itr_time += self.time_delta
            itr_time = self.start_date
        log_file.close()

if __name__ == '__main__':
    d = Generate_Data()
    d.config_assets()
    d.config_tags()
    d.generate_data()

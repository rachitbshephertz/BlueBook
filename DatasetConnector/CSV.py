import pandas as pd
import urllib
import socket


class CSV(object):

    def __init__(self):
        pass

    def dataset(self, db_params):
        dataset = pd.read_csv(db_params["source"])
        return dataset

    def check_connection(self, db_param):
        try:
            return True
            # return urllib.urlopen(db_param["source"], timeout=5).getcode() == 200
        except urllib.URLError as e:
            return False
        except socket.timeout as e:
            return False

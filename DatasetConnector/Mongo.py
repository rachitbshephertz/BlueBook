import pandas as pd
from pymongo import MongoClient
from bson import Code

class Mongo(object):

    def __init__(self):
        pass

    def connect(self,host, port, username, password, db):
        """ A util for making a connection to mongo """

        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = MongoClient(mongo_uri)
        else:
            conn = MongoClient(host, port)

        return conn[db]

    def dataset(self, db_param):
        """ Read from Mongo and Store into DataFrame """

        no_id = True

        # Connect to MongoDB
        conn = Mongo.connect(self, host=db_param["host"], port=db_param["port"],
                             username=db_param["username"], password=db_param["password"],
                             db=db_param["db"])

        # Make a query to the specific DB and Collection
        cursor = conn[db_param["collection"]].find()

        # Expand the cursor and construct the DataFrame
        dataframe = pd.DataFrame(list(cursor))

        # Delete the _id
        if no_id:
            del dataframe['_id']

        return dataframe

    def check_connection(self, db_param):
        pass

    def get_columns(self, db_param):
        client = MongoClient()
        db = client[db_param["db"]]
        map = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        result = db[db_param["collection"]].map_reduce(map, reduce, "myresults")
        return result.distinct('_id')

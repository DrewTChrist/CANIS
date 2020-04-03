import pymongo
from getpass import getpass
from pymongo.errors import OperationFailure, ConnectionFailure


def get_client():
    while True:
        password = getpass(prompt='Database Password: ')
        client = pymongo.MongoClient(
            'mongodb+srv://CANIS:' + password + '@canis-wacmf.azure.mongodb.net/test?retryWrites=true&w=majority')

        try:
            client.admin.command('ismaster')
            break
        except OperationFailure:
            print('\nIncorrect password\n')
        except ConnectionFailure:
            print('\nConnection failed\n')

    print('\nConnection successful\n')
    return client


def get_database(client, db_name):
    return client[db_name]


def get_collection(database, collection_name):
    return database[collection_name]


def insert_into(collection, topic_name, height, width, topic_vertices):
    topic_to_insert = {'Name': topic_name,
                       'Height': height,
                       'Width': width,
                       'Vertices': topic_vertices}

    return collection.insert_one(topic_to_insert)

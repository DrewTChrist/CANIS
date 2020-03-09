from getpass import getpass
import pymongo
from pymongo.errors import OperationFailure, ConnectionFailure


def get_client():

    while True:
        password = getpass()

        client = pymongo.MongoClient('mongodb+srv://CANIS:' + password + '@canis-wacmf.azure.mongodb.net/test?retryWrites=true&w=majority')

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


def insert_into(collection, topic_name, topic_vertices):
    topic_to_insert = {'Name': topic_name,
                        'Vertices': topic_vertices}

    return collection.insert_one(topic_to_insert)

def delete_where(collection, query):
    return collection.delete_one(query)

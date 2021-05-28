import pymongo
from time import gmtime, strftime

databases = pymongo.MongoClient("mongodb://localhost:27017/")
telnet_database = databases['Telnet']
history_collection = telnet_database['History']
logs_collection = telnet_database["Logs"]


def append_new_command_in_database(text_to_append):
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    inserted_object = {"command": text_to_append, "date": current_time}
    history_collection.insert_one(inserted_object)


def print_history_from_database():
    history = history_collection.find({}, {"_id": 0, "command": 1, "date": 1})
    for data in history:
        print(data)


def append_new_log_in_database(sender, subject, text_to_append):
    print("***************************")
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    inserted_object = {"subject": subject, "data": str(text_to_append), "date": current_time}
    print(inserted_object)
    logs_collection.insert_one(inserted_object)





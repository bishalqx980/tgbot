import pymongo
from bot import mongodb_uri, db_name, logger

# connecting to db
client = pymongo.MongoClient(mongodb_uri)
db = client[db_name]

class MongoDB:
    async def insert_single_data(collection_name, data):
        """
        ex. data = {"name": "John", "age": 30, "city": "New York"}
        """
        collection = db[collection_name]

        try:
            logger.info(f"Inserting Single Data in {collection_name} MongoDB...")
            inject = collection.insert_one(data)
            inserted_id = inject.inserted_id
            logger.info(f"Inserted ID: {inserted_id}")
            return inserted_id
        except Exception as e:
            logger.error(e)


    async def insert_multiple_data(collection_name, data_list):
        """
        ex. data = [
            { "name": "Alice", "age": 25, "city": "San Francisco" },
            { "name": "Bob", "age": 28, "city": "Seattle" },
        ]
        """
        collection = db[collection_name]

        try:
            logger.info(f"Inserting Multiple Data in {collection_name} MongoDB...")
            inject = collection.insert_many(data_list)
            inserted_ids = inject.inserted_ids
            logger.info(f"Inserted IDs: {inserted_ids}")
            return inserted_ids
        except Exception as e:
            logger.error(e)


    async def find_one(collection_name, search, match):
        """
        Example: x = find_one(collection_name)\n
        x.get(item)
        """
        collection = db[collection_name]
        
        try:
            logger.info(f"Finding Data in {collection_name} MongoDB...")
            document = collection.find_one({search: match})
            if document:
                logger.info("Data Found: [DATA INFO HIDDEN BECASUE OF DATA PRIVACY]!!")
            else:
                logger.info("Data Not Found!")
            return document
        except Exception as e:
            logger.error(e)
    

    async def find(collection_name, search):
        """
        returns >> only searched data value
        """
        collection = db[collection_name]
        try:
            logger.info(f"Finding Data in {collection_name} MongoDB...")
            documents = collection.find({})
            storage = []
            if documents:
                for document in documents:
                    doc_value = document.get(search)
                    storage.append(doc_value)
                    logger.info("Data Found: [DATA INFO HIDDEN BECASUE OF DATA PRIVACY]!!")
            return storage
        except Exception as e:
            logger.error(e)


    async def get_data(collection_name, get_data):
        collection = db[collection_name]
        try:
            logger.info(f"Getting Data from {collection_name} MongoDB...")
            documents = collection.find_one()
            data = documents.get(get_data)
            if data:
                logger.info("Got Data: [DATA INFO HIDDEN BECASUE OF DATA PRIVACY]!!")
            else:
                logger.info("Data Not Found!")
            return data
        except Exception as e:
            logger.error(e)


    async def update_db(collection_name, search, match, update_data_name, update_data_value):
        collection = db[collection_name]
        try:
            logger.info(f"Updating {collection_name} MongoDB Data...")
            collection.update_one(
                {search: match},
                {"$set": {update_data_name: update_data_value}}
            )
            logger.info(f"{collection_name} MongoDB DATA UPDATED !!")
        except Exception as e:
            logger.error(e)


    async def info_db(collection_name=None):
        docs_name = db.list_collection_names()
        if collection_name:
            logger.info(f"Getting Info about {collection_name} MongoDB...")
            if collection_name in docs_name:
                doc_stats = db.command("collstats", collection_name)
                # stats
                doc_name = collection_name
                doc_count = doc_stats['count']
                doc_size = f"{doc_stats['storageSize'] / (1024 * 1024):.2f} MB"
                doc_acsize = f"{doc_stats['size'] / (1024 * 1024):.2f} MB"
                logger.info("Got Info: [INFO HIDDEN BECASUE OF PRIVACY]!!")
                return doc_name, doc_count, doc_size, doc_acsize
            else:
                logger.info(f"{collection_name} Not found!!")
        else:
            storage = []
            for collection_name in docs_name:
                logger.info(f"Getting Info about {collection_name} MongoDB...")
                doc_stats = db.command("collstats", collection_name)
                # stats
                doc_name = collection_name
                doc_count = doc_stats['count']
                doc_size = f"{doc_stats['storageSize'] / (1024 * 1024):.2f} MB"
                doc_acsize = f"{doc_stats['size'] / (1024 * 1024):.2f} MB"
                storage.append((doc_name, doc_count, doc_size, doc_acsize))
            logger.info("Got Info: [INFO HIDDEN BECASUE OF PRIVACY]!!")
            return storage


    async def delete_all_doc(collection_name):
        collection = db[collection_name]
        try:
            logger.info(f"{collection_name} Data deleting process started...")
            collection.delete_many({})
            logger.info(f"{collection_name} Data Deleted!!")
        except Exception as e:
            logger.error(e)

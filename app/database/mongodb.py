from typing import Union

from pymongo import MongoClient

from app import logger, config


class MongoDatabase:
    SETTINGS = "settings"
    USERS = "users"
    CHATS = "chats"

    def __init__(self):
        self.client = MongoClient(config.mongodb_uri)
        self.database = self.client[config.db_name]
        self.cache = {}


    def _get_cached(self, collection: str, identifier):
        """Return cached document if it exists."""
        return self.cache.get(collection, {}).get(identifier)


    def _set_cached(self, collection: str, identifier, data: dict):
        """Store a complete document in cache."""
        if data is not None:
            self.cache.setdefault(collection, {})[identifier] = data


    def _clear_cached(self, collection: str, identifier=None):
        """Clear one cached document or an entire collection cache."""
        if collection not in self.cache:
            return

        if identifier is None:
            self.cache.pop(collection, None)
        else:
            self.cache[collection].pop(identifier, None)


    def insert(
        self,
        collection: str,
        identifier: Union[str, int] = 0,
        data: dict | None = None,
        cache: bool = True,
    ):
        """
        Insert a document.

        :param collection: Collection name.
        :param identifier: Identifier used for caching.
        :param data: Document to insert.
        :param cache: Whether to cache the inserted document.

        SETTINGS is treated specially and uses the document itself as
        the cache value.
        """

        if data is None:
            data = {}

        try:
            if collection != self.SETTINGS and identifier == 0:
                logger.error(
                    "MongoDB Insert Error: Please double check the identifier!"
                )
                return False

            collection_data = self.database[collection]
            response = collection_data.insert_one(data)

            if not response.acknowledged:
                return False

            # PyMongo adds _id to the original dictionary.
            data["_id"] = response.inserted_id

            if cache:
                if collection == self.SETTINGS:
                    self._set_cached(
                        collection,
                        response.inserted_id,
                        data,
                    )
                else:
                    self._set_cached(
                        collection,
                        identifier,
                        data,
                    )

            return True

        except Exception as e:
            logger.error(e)
            return False


    def search(
        self,
        collection: str,
        search_key,
        match_value,
        cache: bool = True,
    ):
        """
        Find one document.

        :param collection: Collection name.
        :param search_key: Field to search.
        :param match_value: Value to match.
        :param cache: Whether to use/update cache.
        """

        try:
            if cache:
                cached_data = self._get_cached(
                    collection,
                    match_value,
                )

                if cached_data is not None:
                    return cached_data

            collection_data = self.database[collection]

            data = collection_data.find_one({
                search_key: match_value
            })

            if data is not None and cache:
                self._set_cached(
                    collection,
                    match_value,
                    data,
                )

            return data

        except Exception as e:
            logger.error(e)
            return None


    def get_field_values(self, collection: str, search_key):
        """
        Get values of a specific field from every document.
        """

        try:
            collection_data = self.database[collection]

            documents = collection_data.find(
                {},
                {search_key: 1}
            )

            return [
                doc.get(search_key)
                for doc in documents
            ]

        except Exception as e:
            logger.error(e)
            return None


    def update(
        self,
        collection: str,
        search_key,
        match_value,
        data: dict,
        cache: bool = True,
    ):
        """
        Update a document and keep the cache synchronized.
        """

        try:
            collection_data = self.database[collection]

            response = collection_data.update_one(
                {search_key: match_value},
                {"$set": data},
            )

            if not response.acknowledged:
                return False

            if response.matched_count == 0:
                return False

            if cache:
                # Get the complete updated document from MongoDB.
                updated_data = collection_data.find_one({
                    search_key: match_value
                })

                if updated_data is not None:
                    self._set_cached(
                        collection,
                        match_value,
                        updated_data,
                    )

            return True

        except Exception as e:
            logger.error(e)
            return False


    def get_bot_data(
        self,
        collection: str = SETTINGS,
        cache: bool = True,
    ):
        """
        Get the first/single bot document from a collection.

        Intended primarily for the SETTINGS collection.
        """

        try:
            if cache:
                cached_collection = self.cache.get(collection)

                if cached_collection:
                    # SETTINGS normally contains one document.
                    return next(
                        iter(cached_collection.values()),
                        None,
                    )

            collection_data = self.database[collection]

            data = collection_data.find_one({})

            if data is None:
                logger.info(
                    "Bot data wasn't found! "
                    "Please check collection name!"
                )
                return None

            if cache:
                self._set_cached(
                    collection,
                    data["_id"],
                    data,
                )

            return data

        except Exception as e:
            logger.error(e)
            return None


    def database_info(
        self,
        collection: Union[str, list[str]] = None,
    ):
        """
        Get information about one or more collections.
        """

        try:
            if collection:
                collection_list = (
                    [collection]
                    if isinstance(collection, str)
                    else collection
                )
            else:
                collection_list = self.database.list_collection_names()

            final_data = {}

            for collection_name in collection_list:
                collection_info = self.database.command(
                    "collstats",
                    collection_name,
                )

                final_data[collection_name] = {
                    "name": collection_name,
                    "quantity": collection_info["count"],
                    "size": (
                        f'{collection_info["storageSize"] / (1024 * 1024):.2f} MB'
                    ),
                    "acsize": (
                        f'{collection_info["size"] / (1024 * 1024):.2f} MB'
                    ),
                }

            return final_data

        except Exception as e:
            logger.error(e)
            return None


    def delete(
        self,
        collection: str,
        search_key,
        match_value,
        cache: bool = True,
    ):
        """
        Delete a single document.
        """

        try:
            collection_data = self.database[collection]

            response = collection_data.delete_one({
                search_key: match_value
            })

            if not response.acknowledged:
                return False

            if cache and response.deleted_count:
                self._clear_cached(
                    collection,
                    match_value,
                )

            return True

        except Exception as e:
            logger.error(e)
            return False


    def delete_collection(self, collection: str):
        """
        Delete every document in a collection.

        Note: This operation cannot be undone.
        """

        try:
            collection_data = self.database[collection]

            response = collection_data.delete_many({})

            if not response.acknowledged:
                return False

            self._clear_cached(collection)

            return True

        except Exception as e:
            logger.error(e)
            return False


    def clear_cache(self, collection: str = None):
        """
        Clear cache for one collection or the entire database.
        """

        if collection is None:
            self.cache.clear()
        else:
            self._clear_cached(collection)


    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()

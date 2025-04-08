import json
from io import BytesIO
from ... import logger

def fetch_database(database_path="bot/modules/psndl/database.json"):
    """
    :param database_path: `.json` file location
    """
    try:
        with open(database_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(e)

class PSNDL:
    def search(game_name):
        """
        :param game_name: name of the game
        """
        database = fetch_database()
        if not database:
            return
        
        filtered_data = {}

        for game_type in database:
            filtered_type = database.get(game_type)

            for region in filtered_type:
                filtered_region = filtered_type.get(region)

                for game_id in filtered_region:
                    filtered_game_data = filtered_region.get(game_id)

                    if game_name.lower() in filtered_game_data.get("name").lower():
                        check_exist = filtered_data.get(game_type)

                        if check_exist:
                            check_exist.update({game_id: filtered_game_data})
                        else:
                            filtered_data.update({game_type: {game_id: filtered_game_data}})
        
        return filtered_data if filtered_data else None


    def gen_rap(hex_data):
        """
        :param rap_data: hex string e.g(`EE1E8B6E0A737C657A38780B138C403A`)\n
        returns `dict` of data including `.rap` file path
        """
        database = fetch_database()
        if not database:
            return
        
        for game_type in database:
            filtered_type = database.get(game_type)

            for region in filtered_type:
                filtered_region = filtered_type.get(region)

                for game_id in filtered_region:
                    filtered_game_data = filtered_region.get(game_id)
                    database_rap_data = filtered_game_data.get("rap_data")

                    if hex_data.lower() == database_rap_data.lower():
                        rap_name = filtered_game_data.get("rap_name")
                        
                        rap_bytes = BytesIO(bytes.fromhex(database_rap_data))
                        rap_bytes.name = rap_name

                        return {
                            "game_data": filtered_game_data,
                            "rap_bytes": rap_bytes
                        }

import os
import json

JSON_FILE = "bot/modules/psndl/psndl_db.json"

class PSNDL:
    async def search(keyword):
        with open(JSON_FILE, "r") as f:
            load_db = json.load(f)
        
        filtered_data = {}
        for file_type in load_db:
            collection = load_db.get(file_type)
            for region in collection:
                region_data_coll = collection.get(region)

                for game_id in region_data_coll:
                    game_data = region_data_coll.get(game_id)
                    game_name = game_data.get("name")
                    if keyword.lower() in game_name.lower():
                        check_exist = filtered_data.get(file_type)
                        if check_exist:
                            check_exist.update({game_id: game_data})
                        else:
                            filtered_data.update({file_type: {game_id: game_data}})

        if filtered_data == {}:
            return
        else:
            return filtered_data


    async def gen_rap(rap_data):
        with open(JSON_FILE, "r") as f:
            load_db = json.load(f)
        
        for file_type in load_db:
            collection = load_db.get(file_type)
            for region in collection:
                region_data_coll = collection.get(region)

                for game_id in region_data_coll:
                    game_data = region_data_coll.get(game_id)
                    db_rap_data = game_data.get("rap_data")
                    if rap_data == db_rap_data:
                        rap_name = game_data.get("rap_name")
                        os.makedirs("download", exist_ok=True)
                        rap_location = f"download/{rap_name}"
                        with open(rap_location, "wb") as f:
                            f.write(bytes.fromhex(db_rap_data))
                        return game_data, rap_name, rap_location

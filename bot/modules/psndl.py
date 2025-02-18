import json
import aiohttp
from bot import psndl_db, logger

async def get_database():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(psndl_db) as response:
                data = await response.text()
                json_data = json.loads(data)
                return json_data
    except Exception as e:
        logger.error(e)


class PSNDL:
    async def search(keyword):
        database = await get_database()
        if not database:
            return
        
        filtered_data = {}
        for file_type in database:
            collection = database.get(file_type)
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
        database = await get_database()
        if not database:
            return
        
        for file_type in database:
            collection = database.get(file_type)
            for region in collection:
                region_data_coll = collection.get(region)

                for game_id in region_data_coll:
                    game_data = region_data_coll.get(game_id)
                    db_rap_data = game_data.get("rap_data")
                    if rap_data == db_rap_data:
                        rap_name = game_data.get("rap_name")
                        rap_location = f"downloads/{rap_name}"
                        open(rap_location, "wb").write(bytes.fromhex(db_rap_data))
                        return game_data, rap_name, rap_location

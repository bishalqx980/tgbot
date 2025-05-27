import aiohttp
from io import BytesIO
from bot import logger, PSNDL_DATABASE_URL

class PSNDL:
    async def fetch_database():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PSNDL_DATABASE_URL) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            logger.error(e)
    

    async def search(package_name):
        """
        :param package_name: name of the package
        """
        database = await PSNDL.fetch_database()
        if not database:
            return 404
        
        try:
            sortedData = {}

            for packageType in database:
                for packageRegion in database[packageType]:
                    for packageID in database[packageType][packageRegion]:
                        sortedPackageData = database[packageType][packageRegion][packageID]

                        if package_name.lower() in sortedPackageData.get("name").lower():
                            if sortedData.get(packageType):
                                sortedData[packageType].update({packageID: sortedPackageData})
                            else:
                                sortedData.update({packageType: {packageID: sortedPackageData}})
            
            return sortedData if sortedData else 500
        except Exception as e:
            logger.error(e) 


    async def gen_rap(rap_data):
        """
        :param rap_data: hex string e.g(`EE1E8B6E0A737C657A38780B138C403A`)\n
        returns `dict` of data including `.rap` file bytes
        """
        database = await PSNDL.fetch_database()
        if not database:
            return 404
        
        try:
            sortedData = None

            for packageType in database:
                for packageRegion in database[packageType]:
                    for packageID in database[packageType][packageRegion]:
                        sortedPackageData = database[packageType][packageRegion][packageID]

                        rapData = sortedPackageData.get("rap_data")

                        if rap_data.lower() == rapData.lower():
                            rapName = sortedPackageData.get("rap_name")
                            
                            rapBytes = BytesIO(bytes.fromhex(rapData))
                            rapBytes.name = rapName

                            sortedData = {"packageData": sortedPackageData, "rapBytes": rapBytes}
                            if sortedData: break
                    if sortedData: break
                if sortedData: break
            
            return sortedData if sortedData else 500
        except Exception as e:
            logger.error(e)

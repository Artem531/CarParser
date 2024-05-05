import re

def normalizeString(str):
    def tmp(string):
       return re.sub("[^a-zA-Zа-яА-ЯёЁ]", "", string)
    return tmp(str).lower()

def getPriceFromDB(priceFromDB):
    """
    :param priceFromDB: data_i["Цена"]
    :return: price
    """
    if (priceFromDB == 'Po dogovoru' or priceFromDB == 'Na upit'):
        return None
    return int(filterGarbageFromDigital(priceFromDB))

def filterGarbageFromDigital( str_digit ):
    return re.sub("[^0-9]", "", str_digit.split("€")[0])

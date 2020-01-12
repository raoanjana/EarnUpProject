import sys
import mysql.connector
from decimal import *
from geopy.distance import great_circle

#"{latitude:40.7306,longitude:-73.9352,distance:7,price:900,neighbourhood:Chinatown,room_type:Private room}"


def prepare_search_dict(search_dict_entry):
    search_dict = {}
    for arg in search_dict_entry:
        dict_entry = arg.split(":")
        dict_entry[0] = dict_entry[0].replace(' ', '')
        search_dict[dict_entry[0]] = dict_entry[1]
    return search_dict


#builds queries based off of entered search parameters
def build_query(neighbourhood, price, room_type):
    query = "SELECT ID,NAME, HOST_NAME, PRICE, NEIGHBOURHOOD,LATITUDE, LONGITUDE FROM ROOM_LOC "
    if neighbourhood != '':
        neighbour_q = "WHERE ROOM_LOC.NEIGHBOURHOOD = %s "
        query = query + neighbour_q
    if price != 0:
        price_q = "AND ROOM_LOC.PRICE <= %s "
        query = query + price_q
    if room_type != '':
        room_q = "AND ROOM_LOC.ROOM_TYPE = %s"
        query = query + room_q
    return query



#return record of rooms that
def search_rooms(lat1, long1, distance, neighbourhood, price, room_type, mycursor):
    search_results = []
    query = build_query(neighbourhood, price, room_type)

    mycursor.execute(query,(neighbourhood, price, room_type, ))
    records = mycursor.fetchall()
    for record in records:
        distTo = int(great_circle((lat1,long1),(record[5], record[6])).miles)
        if (distTo <= distance):
            result = ({'id': record[0], 'name': record[1], 'host': record[2], 'distance': distTo, 'price': record[3], 'neighbourhood':record[4]})
            print result
            search_results.append(result)
    return search_results
#runs search query
def main():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="DB123access",
        database="AB_NYC"

    )
    mycursor = mydb.cursor(prepared=True)

    search_dict_str = sys.argv[1]
    search_dict_str = search_dict_str.replace('{', '')
    search_dict_str = search_dict_str.replace('}', '')
    search_dict_entry = search_dict_str.split(",")
    search_dict = prepare_search_dict(search_dict_entry)

    lat1 = Decimal(search_dict['latitude'].replace(' ', ''))
    long1 = Decimal(search_dict['longitude'].replace(' ', ''))
    distance = int(search_dict['distance'].replace(' ', ''))
    if 'price' in search_dict:
        print search_dict['price']
        price = int(search_dict['price'].replace(' ', ''))
    if 'neighbourhood' in search_dict:
        neighbourhood = search_dict['neighbourhood'].replace(' ', '')
    if 'room_type' in search_dict:
        room_type = search_dict['room_type']

    search_rooms(lat1, long1,distance,  neighbourhood, price, room_type, mycursor)

if __name__ == "__main__":
    main()
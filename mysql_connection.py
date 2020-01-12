import csv
import sys

import mysql.connector

# establishes database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="DB123access",
    database="AB_NYC"

)
mycursor = mydb.cursor()

#execute sql script to create database and table
def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                mycursor.execute(command)
        except IOError, msg:
            print "Command skipped: ", msg


executeScriptsFromFile('/Users/anjana.rao/PycharmProjects/EarnUpProject/ABNYC.db')


col_list = ['id', 'name', 'host_id', 'host_name', 'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude',
          'room_type', 'price', 'minimum_nights', 'number_of_reviews', 'last_review', 'reviews_per_month',
          'calculated_host_listings_count', 'availability_365']
filename = "AB_NYC_2019.csv"
f = open('AB_NYC_2019.csv', "rb")
reader = csv.reader((line.replace('\0', '0') for line in f),delimiter=',', quotechar='"') #replaces null with 0


query = "INSERT INTO room_loc(id,name,host_id,host_name,neighbourhood_group,neighbourhood,latitude,longitude,room_type,price,minimum_nights,number_of_reviews,last_review,reviews_per_month,calculated_host_listings_count,availability_365)" \
        "VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"

#open and read csv file for data
filename = "AB_NYC_2019.csv"
f = open('AB_NYC_2019.csv', "rb")
reader = csv.reader((line.replace('\0', '') for line in f),delimiter=',', quotechar='"')

#col_list = list(next(reader))

next(reader)
for row in reader:
    for i in range(len(row)):
        if row[i] is "":
            row[i] = 0
        if col_list[i] == "latitude" or col_list[i]== "longitude":
            try: #checks if lat or long is a float
                row[i] = float(row[i])
            except: #skips line if it is corrupt
                print("Could not convert data to an integer. Skipped",row[0],"id.")
                if next(reader):
                    row = next(reader)
    try:
        mycursor.execute(query, row)
    except:
        print("Could not insert",mycursor.rowcount,"row(s) of data.")
mydb.commit()







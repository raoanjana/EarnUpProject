# EarnUpProject
NYC Room Search Engine 


EarnUp project provides an API for users to search rooms in NYC with a given location and distance by querying through a database that stores room information. 

Prior to running search_rooms.py, the database should be populated with the room csv data. "mysql_connection.py" ingests csv data, populates the database with the rows excluding rows without latitude or longitude and fixing any null values. 

Since it is an API for the purpose of the project, search_rooms.py contains the functionality of the API and can be executed via command line by running the script with a search query:
"Python search_rooms.py {latitude:40.7306,longitude:-73.9352,distance:7,price:900,neighbourhood:Chinatown,room_type:Private room}"


Following filters are available for the query:
Distance (required), Latitude (required), Longitude (required), Price, (optional), Room Type (optional), Neighbourhood (optional). 

Along with the required filters, atleast one of the following optional filters must also be specified for the query.

The response is stored in a list of dictionaries containing the query results stored in "search_results" For demo purposes, the script also prints out the results once the api is executed. 

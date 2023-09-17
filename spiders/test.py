from geopy.geocoders import Bing

g = Bing(api_key='AkEMqkI71pVf7n-ftGrtg25gS75q-P1WhjbsD_eh8BSL3ntMlYJeYFoAGqhXYPCI')
l = g.geocode("75 University Ave. West Waterloo ON N2L 3C5")
print(l.raw)
# print(l.raw['point']['coordinates'][0])
# print(l.raw['point']['coordinates'][1])
# print(l.raw['address']['locality'])
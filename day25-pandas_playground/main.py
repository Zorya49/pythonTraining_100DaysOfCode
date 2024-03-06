# with open("weather_data.csv") as file:
#     data = file.readlines()
#     for _ in data:
#         print(_)

# import csv
# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     temperature = []
#     for row in data:
#         print(row)
#         if row[1] != "temp":
#             temperature.append(int(row[1]))
#
#     print(temperature)

import pandas

# data = pandas.read_csv("weather_data.csv")
# print(data["temp"])
# print(type(data))
# print(type(data["temp"]))
#
# temperature_list = data["temp"].tolist()
# avg_temp = sum(temperature_list) / len(temperature_list)
# print(f"Avg. temperature = {avg_temp}")
# print(f"Avg. temperature from pandas lib = {data["temp"].mean()}")
# print(f"Max. temperature from pandas lib = {data["temp"].max()}")
#
# # Get data from columns
# print(data["condition"])
# print(data.condition)

# # Get data from rows
# print(data[data.day == "Monday"])
# print(data[data.temp == data.temp.max()])
#
# monday = data[data.day == "Monday"]
# print(monday.condition)
# print(f"Monday's temperature was {monday.temp[0] * 1.8 + 32}")

# # Create data from file
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
#
# scores_data = pandas.DataFrame(data_dict)
# print(scores_data)
#
# scores_data.to_csv("new_data.csv")


squirrel_data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
squirrels = squirrel_data["Primary Fur Color"].value_counts()
squirrels.to_csv("squirrel_count_data.csv")
print(squirrels)

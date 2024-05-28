# import requests
# import json
# import os

# import hbclass



# base_url = "http://192.168.1.43:3100/api/v1/"
# user = "ron%40brunij.nl"
# password = "01%5E5Mei2006"
# loc_folder = "/Users/rbruins/Downloads/homebox/locations"

# hb = hbclass.HomeboxApi(user,password,base_url)

# def main():
#     #mv_loc_parent_item()
#     label_id = "2070e5f5-7e53-4aa6-bf87-a07b9e3b0d18"
#     update_label(label_id)


# def update_label(label_id):
#     items = hb.get_items()
#     for item in items['items']:
#         #if "Feestje Twan" in item['name']:
#         #print("FOUND")

#         item_details = hb.get_item_by_id(item['id'])
#         #print(item_details['parent']['id'])
#         name = item['name']
#         item_id = item['id']
#         try:
#             parent_item_id = item_details['parent']['id']
#             location_id = item['location']['id']
#             print(f"Name: {name}")
#             print(f"id: {item_id}")
#             print(f"ParId: {parent_item_id}")
#             print(f"LocId: {location_id}")
#             hb.update_item_label(parent_item_id,item_id,location_id,name)
#         except:
#             pass

# def mv_loc_parent_item():
#     locations = hb.get_location()
#     for location in locations:
#         if "IKEA Box 1" in location['name']:
#             print(location)
#             print(location['name'],location['id'])
#             location_id = location['id']
#             parent_item_id = hb.create_item(location_id,location['name'])
#     items = hb.get_items()
#     for item in items['items']:
#         if location_id == item['location']['id']:
#             print(item['name'])
#             print(item['id'])
#             hb.update_item(parent_item_id,item['id'],location_id,item['name'])


# if __name__ == '__main__':
#     main()

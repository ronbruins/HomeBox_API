import os
import hbclass
import settings

base_url = settings.base_url
user = settings.user
password = settings.password
loc_folder = settings.loc_folder

hb = hbclass.HomeboxApi(user,password,base_url)

def main():
    get_file_list()

def get_file_list():
    loc_idx = 0
    for root, dirs, files in os.walk(loc_folder):
        for sublevel in dirs:
            print(loc_idx,sublevel)
            if loc_idx == 0:
                location = sublevel
                location_id = do_location(location)
            else:
                print(f"{sublevel} is parent item")
                parent_itemname = sublevel
                parent_item_id,item_location = do_parent_item(parent_itemname,location_id,location)
                print(parent_item_id,item_location)
                loop_item(location_id,item_location,parent_item_id)
            loc_idx = loc_idx + 1
            

def do_location(location):
    print(f"Location: {location}")
    locations = hb.get_location()
    loc_exists = False
    for existing_location in locations:
        if location == existing_location['name']:
            print("location exists, not recreating")
            location_id = existing_location['id']
            loc_exists = True
    if loc_exists == False:
        print(f"create location {location}")
        location_id = hb.create_location(location)
    return location_id

def do_parent_item(parent_itemname,location_id,location):
    parent_item_id = hb.create_item(location_id,parent_itemname)
    pic_name = f"{parent_itemname}.jpeg"
    item_location = f"{loc_folder}/{location}/{parent_itemname}"
    hb.upload_photo(parent_item_id,pic_name,item_location)
    return parent_item_id,item_location

def loop_item(location_id,item_location,parent_item_id):
    for root, dirs, files in os.walk(item_location):
        for item in files:
            if ".DS_Store" not in item:
                itemname = item.split('.')
                itemname = itemname[0]
                print(f"itemname: {itemname}")
                print(f"Item: {item}")
                print(f"itemlocation: {item_location}")
                if itemname not in item_location:
                    item_id = hb.create_item(location_id,itemname)
                    hb.upload_photo(item_id,item,item_location)
                    hb.update_item(parent_item_id,item_id,location_id,itemname)

if __name__ == '__main__':
    main()

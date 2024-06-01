import os
import hbclass
import settings
import json
import subprocess

base_url = settings.base_url
user = settings.user
password = settings.password
loc_folder = settings.loc_folder
ssc_path = "/usr/local/bin/exiftool"

hb = hbclass.HomeboxApi(user,password,base_url)

def main():
    do_location_folder()
    #mv_loc_parent_item()
    #label_id = "2070e5f5-7e53-4aa6-bf87-a07b9e3b0d18"
    #update_label(label_id)
    # label_id = hb.create_label("testlabel")
    # print(label_id)

def do_location_folder():
    loc_idx = 0
    for root, dirs, files in os.walk(loc_folder):
        for sublevel in dirs:
            if loc_idx == 0:
                location = sublevel
                location_id = do_location(location)
            else:
                parent_itemname = sublevel
                parent_item_id,item_location = do_parent_item(parent_itemname,location_id,location)
                loop_item(location_id,item_location,parent_item_id)
            loc_idx = loc_idx + 1
            

def do_location(location):
    print(f"Location: {location}")
    locations = hb.get_location()
    loc_exists = False
    for existing_location in locations:
        if location == existing_location['name']:
            location_id = existing_location['id']
            loc_exists = True
    if loc_exists == False:
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
                if itemname not in item_location:
                    item_id = hb.create_item(location_id,itemname)
                    hb.upload_photo(item_id,item,item_location)
                    hb.update_item(parent_item_id,item_id,location_id,itemname)

                    exif_json = call_ssc(f"{item_location}/{item}")
                    for exifinfo in exif_json:
                        raw_taglist = exifinfo['XMP:TagsList']
                        labels = []
                        labelids = []
                        taglist = []
                        if type(raw_taglist) != list:
                            taglist.append(raw_taglist)
                        else:
                            taglist = raw_taglist
                        for tag in taglist:
                            print(tag)
                            label_check = hb.get_labels()
                            label_found = False
                            for label in label_check:
                                label_name = label['name']
                                label_id = label['id']
                                if tag in label_name:
                                    label_found = True
                                    label_det = {"id":label_id,"name":label_name}
                                    labels.append(label_det)
                                    labelids.append(label_id)
                                    print(f"{item} with {tag} found in labels as ### {label_name}, {label_id}")
                            if label_found == False:
                                print(f"{item} with {tag} not found in labels")
                                label_id = hb.create_label(tag)
                                label_det = {"id":label_id,"name":tag}
                                labels.append(label_det)
                                labelids.append(label_id)
                    print(labels)
                    print(labelids)
                    hb.update_item_label(parent_item_id,item_id,location_id,itemname,labels,labelids)



def update_label(label_id):
    items = hb.get_items()
    for item in items['items']:
        #if "Feestje Twan" in item['name']:


        item_details = hb.get_item_by_id(item['id'])
        #print(item_details['parent']['id'])
        name = item['name']
        item_id = item['id']
        try:
            parent_item_id = item_details['parent']['id']
            location_id = item['location']['id']
            print(f"Name: {name}")
            print(f"id: {item_id}")
            print(f"ParId: {parent_item_id}")
            print(f"LocId: {location_id}")
            hb.update_item_label(parent_item_id,item_id,location_id,name)
        except:
            pass

def mv_loc_parent_item():
    locations = hb.get_location()
    for location in locations:
        if "RBTEstBox" in location['name']:
            print(location)
            print(location['name'],location['id'])
            location_id = location['id']
            parent_item_id = hb.create_item(location_id,location['name'])
    items = hb.get_items()
    for item in items['items']:
        if location_id == item['location']['id']:
            print(item['name'])
            print(item['id'])
            hb.update_item(parent_item_id,item['id'],location_id,item['name'])


def call_ssc(FileLoc):
    cmd = "-j -G -n"
    ssc_exec = f"{ssc_path} {cmd} '{FileLoc}'"
    output = str(subprocess.check_output(f"{ssc_exec}", shell=True, encoding='utf-8',stderr=subprocess.DEVNULL))
    output = os.linesep.join([s for s in output.splitlines() if s])
    #print(output)
    return json.loads(output)

if __name__ == '__main__':
    main()

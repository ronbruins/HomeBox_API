import requests
import json

class HomeboxApi:
    def __init__(self,user,password,base_url):
        self.user = user
        self.password = password
        self.base_url = base_url
        self.token = self.login()
        self.payload = {}

    def login(self):
        api = "users/login"
        url = self.base_url + api
        payload = f'username={self.user}&password={self.password}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        hbresponse = json.loads(response.text)
        token = hbresponse['token']
        #print(token)
        return token
    
    def get_location(self):
        api = "locations"
        method = "GET"
        json_data = ""
        locations = self.hb_post(method,api,json_data)
        return locations
    
    def get_location_by_id(self,location_id):
        api = f"locations/{location_id}"
        method = "GET"
        json_data = ""
        locations = self.hb_post(method,api,json_data)
        return locations

    def get_items(self):
        api = "items"
        method = "GET"
        json_data = ""
        items = self.hb_post(method,api,json_data)
        return items
        
    def get_item_by_id(self,item_id):
        api = f"items/{item_id}"
        method = "GET"
        json_data = ""
        items = self.hb_post(method,api,json_data)
        return items


    def create_location(self,location):
        api = "locations"
        method = "POST"
        json_data = {
            "description": None,
            "name": f"{location}",
            "parentId": None
            }
        location_id = self.hb_post(method,api,json_data)
        return location_id

    def create_item(self,location_id,name):
        api = "items"
        method = "POST"
        json_data = {
            'description': None,
            'labelIds': [],
            'locationId': f'{location_id}',
            'name': f'{name}',
            'parentId': None,
        }
        item_id = self.hb_post(method,api,json_data)
        return item_id

    def update_item(self,parent_item_id,item_id,location_id,name):
        api = f"items/{item_id}"
        method = "PUT"
        json_data = {
            "id":f"{item_id}",
            "name":f"{name}",
            "locationId":f"{location_id}",
            "parentId":f"{parent_item_id}"
            }
        item_id = self.hb_post(method,api,json_data)
        return item_id

    def get_labels(self):
        api = "labels"
        method = "GET"
        json_data = ""
        labels = self.hb_post(method,api,json_data)
        return labels


    def create_label(self,name):
        api = "labels"
        method = "POST"
        json_data = {
            "name": f"{name}"
            }
        label_id = self.hb_post(method,api,json_data)
        return label_id


    def update_item_label(self,parent_item_id,item_id,location_id,name,labels,labelids):
        api = f"items/{item_id}"
        method = "PUT"
        json_data = {
            "id":f"{item_id}",
            "name":f"{name}",
            #"labels":[{"id":"e79a3812-54a4-4aff-abc6-b36e75f0f07c","name":"VSlabel"},{"id":"7d20699f-1fae-4cc4-acb4-f50df48e248b","name":"Feest"}],
            "labels":labels,
            "locationId":f"{location_id}",
            "parentId":f"{parent_item_id}",
            #"labelIds": ["e79a3812-54a4-4aff-abc6-b36e75f0f07c","7d20699f-1fae-4cc4-acb4-f50df48e248b"]
            "labelIds": labelids
            }
        #"labelIds": ["string"],
        #print(f"self.hb_post({method},{api},{json_data}")
        item_id = self.hb_post(method,api,json_data)
        return item_id


    def upload_photo(self,item_id,item,item_location):
        api = f"items/{item_id}/attachments"
        fp = f"{item_location}/{item}"
        method = "POST"
        files_data = {
            'file': (f'{item}', open(fp, 'rb'), 'image/jpeg'),
            'type': (None, 'photo'),
            'name': (None, f'{item}'),
        }
        upload_post = self.hb_post(method,api,files_data)

    def hb_post(self,method,api,json_data):
        url = self.base_url + api
        headers = {
            'Authorization': f'{self.token}',
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if "attachments" in api:
            headers = {
            'accept': 'application/json',
            'Authorization': f'{self.token}',
            }
            response = requests.request(method, url, headers=headers, files=json_data)
        else:
            if method == "GET":
                response = requests.request(method,url, headers=headers)
                response = json.loads(response.text)
                return response
            else:
                response = requests.request(method,url, headers=headers, json=json_data)
                item = json.loads(response.text)
                item_id = item['id']
                return item_id
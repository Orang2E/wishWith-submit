import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    def insert_item(self, name, data, img_path):
        item_info = {
            "product_description": data['product_description'],
            "product_place": data['product_place'],
            "product_number": data['product_number'],
            "product_category": data['product_category'],
            "start_date": data['start_date'],
            "end_date": data['end_date'],
            "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True
    
    def get_items(self ):
        items = self.db.child("item").get().val()
        return items
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""

        print("###########", name)

        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()

        return target_value

    


    
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "name": data['name']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###", users.val())
        if str(users.val()) == "None":  # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True
        

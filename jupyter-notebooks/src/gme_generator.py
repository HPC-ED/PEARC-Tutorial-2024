import json

class GMetaEntry:
    datatype = "GMetaEntry"

    def __init__(self, file_name, subject):
        # Fields required by Globus
        self.file_name = file_name
        self.subject = subject

        self.id = "std"
        self.visibility = '["public"]'

        self.content = {}

    def set_visibility(self, vis):
        self.visibility = vis

    def add_content(self, field, value):
        self.content[field] = value

    def remove_content(self, field):
        del self.content[field]
    
    def show_gme(self):
        gmetaentry = {
            "ingest_type": "GMetaEntry",
            "ingest_data": {
                "subject": self.subject,
                "visible_to": self.visibility,
                "id": self.id,
                "content": self.content
            }
        }
        print(json.dumps(gmetaentry, indent=4))
    
    def create_json(self):
        gmetaentry = {
            "ingest_type": "GMetaEntry",
            "ingest_data": {
                "subject": self.subject,
                "visible_to": self.visibility,
                "id": self.id,
                "content": self.content
            }
        }
        json.dump(gmetaentry, open(f'{self.file_name}.json', 'w'), indent=4)

        with open(f'{self.file_name}.json', 'r') as file:
            data = json.load(file)
            print(json.dumps(data, indent=4))


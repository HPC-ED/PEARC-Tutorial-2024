import json

def parse_text_file(file_path):
    content = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                key, value = line.split(":", 1)
                key = key.strip().strip('"')
                value = value.strip().strip('"')
                if "," in value:
                    value = [v.strip().strip('"') for v in value.split(",")]
                content[key] = value
    return content

def create_gmetaentry(content):
    gmetaentry = {
        "ingest_type": "GMetaEntry",
        "ingest_data": {
            "subject": content.pop("subject"),
            "visible_to": content.pop("visible_to"),
            "id": content.pop("id"),
            "content": content
        }
    }
    return gmetaentry

def main():
    file_path = input("Enter the path to the text file: ")
    content = parse_text_file(file_path)
    gmetaentry = create_gmetaentry(content)
    gmetaentry_json = json.dumps(gmetaentry, indent=4)
    print("GMetaEntry JSON Document:")
    print(gmetaentry_json)

if __name__ == "__main__":
    main()

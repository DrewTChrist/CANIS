import json
import modules.database_link as dbl
from modules.knowledge_extractor import thin_vertices


class Topic:

    def __init__(self, label, vertices):
        self.label = label
        self.vertices = vertices


def knowledge_base():
    try:
        # If knowledgebase.json exists, try to open it and parse it
        with open('knowledgebase.json', 'r') as f:
            knowledgebase = json.load(f)

        print("Loading knowledgebase file...")
        knowledge = []
        for k in knowledgebase:
            knowledge.append(Topic(k[0], k[1]))

        return knowledge
    except:
        # knowledgebase.json does not exist, generate it from the database
        print("Generating knowledgebase file...")
        client = dbl.get_client()
        db = client['CANIS_DB']
        topics = db['Topics']
        collection = topics.find()
        knowledge = []
        for topic in collection[1:]:
            knowledge.append(Topic(topic['Name'], thin_vertices(topic['Vertices'], int(topic['Height']), int(topic['Width']), reduce_to=1)))

        client.close()

        with open('knowledgebase.json', 'w') as f:
            json.dump(knowledge, f, default=lambda x: [x.label, x.vertices])

        return knowledge

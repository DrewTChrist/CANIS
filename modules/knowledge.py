"""Load knowledge_base.json information, or generate it if not found."""
import json

import modules.database_link as dbl
from modules.knowledge_extractor import thin_vertices


class Topic:

    def __init__(self, label, vertices):
        self.label = label
        self.vertices = vertices


def knowledge_base():
    try:
        with open('knowledge_base.json', 'r') as f:
            loaded = json.load(f)

        knowledge = []
        for k in loaded:
            knowledge.append(Topic(k[0], k[1]))

        return knowledge

    except FileNotFoundError:
        client = dbl.get_client()
        db = client['CANIS_DB']
        topics = db['Topics']
        collection = topics.find()

        knowledge = []
        for topic in collection[1:]:
            knowledge.append(Topic(topic['Name'], thin_vertices(topic['Vertices'], topic['Height'], topic['Width'], reduce_to=20)))

        client.close()

        with open('knowledge_base.json', 'w') as f:
            json.dump(knowledge, f, default=lambda x: [x.label, x.vertices])

        return knowledge

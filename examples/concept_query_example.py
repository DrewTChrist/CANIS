import os
import sys

from modules.concept_query import ConceptInquirer

sys.path.append(os.getcwd())

topic = input('Enter a topic: ')
ci = ConceptInquirer(topic)
relationships = ci.get_IsA_nodes()

for relation in relationships.items():
    print(relation)

import os, sys
sys.path.append(os.getcwd())
from modules.concept_query import ConceptInquirer

topic = input('Enter a topic: ')

ci = ConceptInquirer(topic)

relationships = ci.get_IsA_nodes()

for relation in relationships.items():
    print(relation)
import os
import importlib.util

# Loads module from parent directory until we restructure the files
# Snippet from:
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
spec = importlib.util.spec_from_file_location("ConceptInquirer", os.getcwd() + "\concept_query.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


topic = input('Enter a topic: ')

ci = module.ConceptInquirer(topic)

relationships = ci.get_IsA_nodes()

for relation in relationships.items():
    print(relation)
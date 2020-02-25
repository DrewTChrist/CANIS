import os
import importlib.util

# Loads module from parent directory until we restructure the files
# Snippet from:
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
spec = importlib.util.spec_from_file_location("ConceptInquirer", os.getcwd() + "\ConceptInquirer.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


ci = module.ConceptInquirer('dog')

relationships = ci.get_is_a_relationships()

for r in relationships:
    print(r)
import os
import sys

import modules.database_link as dbl

sys.path.append(os.getcwd())

client = dbl.get_client()
db = client['CANIS_DB']
topics = db['Topics']
print(topics.count_documents({}))

client.close()

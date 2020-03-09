import os, sys
sys.path.append(os.getcwd())
import modules.database_link as dbl


client = dbl.get_client()

db = client['CANIS_DB']

topics = db['Topics']

print(topics.count_documents({}))



client.close()
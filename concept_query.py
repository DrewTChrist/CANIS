'''ConceptInquirer class gathers information from ConceptNet to use for name
generation.
'''


import json
import urllib.request


class ConceptInquirer:

    def __init__(self, node):
        self.node_url = self._build_query(node)
        self.json_body = json.loads(
            self._get_response_text(
                self.node_url))

    # Returns a dictionary of nodes connected to the node of the class by an
    # "Is A" relationship and their weights
    def get_is_a_relationships(self):
        relation_dict = {}

        for edge in self.json_body['edges']:
            relation_dict[edge['start']['label']] = edge['weight']

        return relation_dict

    # Builds a url to query conceptnet where node is the end and the nodes
    # returned share an "Is A" relationship with node
    def _build_query(self, node):
        return 'http://api.conceptnet.io/query?end=/c/en/' + \
            node + '&rel=/r/IsA&limit=1000'

    # Simple method to return response from conceptnet
    def _get_response_text(self, node_url):
        request = urllib.request.urlopen(node_url)
        return request.read()

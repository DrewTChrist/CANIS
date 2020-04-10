"""ConceptInquirer class gathers information from ConceptNet to use for name
generation.
"""
import json
import urllib.request
from enum import Enum


class ConceptInquirer:

    def __init__(self, node_topic):
        self.node = node_topic

    # Changes the topic node of the class
    def change_topic(self, new_topic):
        self.node = new_topic

    # Dog is related to pet
    def get_RelatedTo_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.RelatedTo, self.NodeType.START, limit)

    # Dogged is a form of dog
    def get_FormOf_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.FormOf, self.NodeType.END, limit)

    # A poodle is a dog
    def get_IsA_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.IsA, self.NodeType.END, limit)

    # Legs are part of dog
    def get_PartOf_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.PartOf, self.NodeType.END, limit)

    # A dog has four legs
    def get_HasA_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.HasA, self.NodeType.START, limit)

    # A dog is used for running after the ball
    def get_UsedFor_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.UsedFor, self.NodeType.START, limit)

    # A dog is capable of bark
    def get_CapableOf_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.CapableOf, self.NodeType.START, limit)

    # A location of dog is a kennel
    def get_AtLocation_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.AtLocation, self.NodeType.START, limit)

    # A hurricane causes a disaster
    def get_Causes_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.Causes, self.NodeType.START, limit)

    # Dog is has a subevent of pee against trees
    def get_HasSubevent_nodes(self, limit=10):
        return self._get_relationships(self.QueryType.HasSubevent, self.NodeType.START, limit)


    # Methods below this are not meant to be used outside of the class
    # Methods above are meant to give easy access to retrieving information
    # from conceptnet


    # This method returns END if the node_type is START and the other way around
    # Because an end node is usually concerned with the start node
    # and a start node is usually concerned with the end node
    def _reverse_node_type(self, node_type):
        if node_type.value == 1:
            return self.NodeType.END
        else:
            return self.NodeType.START

    # Creates a dictionary from the relationships and their respective weights
    # If we describe an end node it looks to the start node or if we describe
    # a start node it looks to the end node, hence the reverse method
    def _get_relationships_dictionary(self, json_response, node_type):
        reversed_node_type = self._reverse_node_type(node_type)
        relation_dict = {}

        for edge in json_response['edges']:
            relation_dict[edge[reversed_node_type.name.lower()]['label']] = edge['weight']

        return relation_dict

    # This method does the work of getting relationships by using methods
    # needed to retrieve them
    def _get_relationships(self, query_type, node_type, limit=10):
        self.query_url = self._build_query(query_type, node_type, limit)
        response = json.loads(self._get_response_text(self.query_url))
        return self._get_relationships_dictionary(response, node_type)

    # Builds a url to query conceptnet based on the relationship
    # defined by query_type, and if the node is a start or an end
    def _build_query(self, query_type, node_type, limit=10):
        return 'http://api.conceptnet.io/query?' + node_type.name.lower() + \
                '=/c/en/' + self.node + '&rel=/r/' + query_type.name + \
                '&limit=' + str(limit)

    # Simple method to return response from conceptnet
    def _get_response_text(self, node_url):
        request = urllib.request.urlopen(node_url)
        return request.read()

    # Defines relationships used for conceptnet queries
    class QueryType(Enum):
        RelatedTo = 1
        FormOf = 2
        IsA = 3
        PartOf = 4
        HasA = 5
        UsedFor = 6
        CapableOf = 7
        AtLocation = 8
        Causes = 9
        HasSubevent = 10

    # Used to identify starting nodes and end nodes
    class NodeType(Enum):
        START = 1
        END = 2

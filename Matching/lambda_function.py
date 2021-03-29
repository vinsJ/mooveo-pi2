# Here, we'll read our files and make the matching based on severals inputs.

import json
from math import e
import sys

import Heuristics as mainH  # pylint: disable=import-error

from DB import db_loader

listUsers = db_loader.load_user()


def main(id_offer):
    """ Compute scores for all users given an offer

    :param: id_offer

    :return: Stringify object, sent to the client 
    """
    offer = db_loader.load_offer(id_offer)
    res = []
    if(offer):
        if(len(listUsers) > 0):
            for user in listUsers:
                res.append(mainH.computeHeurisitcs(user, offer))
            return json.dumps({'status': 200, 'message': 'OK', 'body': res})
        else:
            return json.dumps({'status':404, 'message': 'No user found in database'})
    else:
        return json.dumps({'status': 404, 'message': 'Offer not found in database'})

def lambda_handler(event, context):
    """ Handle incoming requests

    :return: Stringify object, sent to the client 
    """
    if(event):
        try:
            if(event['id_offer']):
                return main(event['id_offer'])
            else:
                return json.dumps({'status': 404, 'message': 'No id_offer found'})
        except:
            return json.dumps({'message':event, 'status': 403})
    else:
        return json.dumps({'message': 'No body provided', 'status': 403})
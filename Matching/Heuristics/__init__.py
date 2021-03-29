""" Init file, called in lambda_function

Compute the scores for the different criteria

:imports: files in Heuristics

:return: json object (dictionary) containing all the scores.

How to add and use dependencies ?

>>> from . import [file] as [name]
>>> [nameHeuristic] = [name].[functionName]

"""


#from . import disponibility as dipoH
from . import languages as langH
from . import skills as skillsH

from . import distance as distanceH


def computeHeurisitcs(user, offer):
    """ Call method to compute scores from different files

    :param: user: user object
    :param: offer: offer object

    (find the model in DB > model)

    :return: json object (dictionary) containing all the scores.
    """
    try:

        distanceHeuristic = 1
        skillsHeursitic = 1
        languagesHeuristic = 1

        if(user.location):
            distanceHeuristic = distanceH.Heuristic(
                user.location, offer.location)

        if(user.skills):
            skillsHeursitic = skillsH.Heuristic(user.skills, offer.skills)

        if(user.languages):
            languagesHeuristic = langH.Heuristic(
                user.languages, offer.languages)

        return {'user_id': user.id, 'heuristics': {'distance': distanceHeuristic, 'disponibility': 1, 'languages': languagesHeuristic, 'skills': skillsHeursitic}}

    except:
        return {'user_id': user.id, 'heuristics': {'distance': 0, 'disponibility': 0, 'languages': 0, 'skills': 0}}

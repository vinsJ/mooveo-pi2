# Skills heuristic 
import os
from dotenv import load_dotenv

load_dotenv()

MAX_GRADE_USER = int(os.getenv('MAX_GRADE_USER'))

def Heuristic(userSkills, offerSkills):
    """ Skills heurstic

    :param: userSkills: array of skills
    :param: offerSkills: array or skills

    If a user don't have any skills, it'll return 0

    :return: score [0,1], 1: user have all the expected skills | 0 none of the expected skills
    """
    try:
        NBSkills=0
        totalRank = 0
        if(len(userSkills) > 0):
            for offer_skill, ranking in offerSkills.items():
                if(offer_skill in userSkills):
                    NBSkills += userSkills[offer_skill]*ranking
                totalRank += ranking * MAX_GRADE_USER
            if(totalRank == 0):
                return 0
            return (NBSkills / totalRank)
        else:
            return 0
    except:
        return 0
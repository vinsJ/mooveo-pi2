# Languages heuristic 

def Heuristic(userLanguages, offerLanguages):
    """ Languages heurstic

    :param: userLanguages: array of languages
    :param: offerLanguages: array or languages

    :return: score [0,1], 1: user have all the expected languages | 0 none of the expected languages
    """
    try:
        NBLanguage = 0
        if(len(userLanguages) > 0):
            for offers_language in offerLanguages:
                if(offers_language in userLanguages):
                    NBLanguage+=1
            return NBLanguage/len(offerLanguages)
        else:
            return 0
    except:
        return 0
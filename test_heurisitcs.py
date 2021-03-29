import unittest

from Matching.Heuristics import skills
from Matching.Heuristics import languages
from Matching.Heuristics import distance

class Test_get_token(unittest.TestCase):
    """ Testing area

    Please be sure to cd into Matching before executing, otherwise,
    Heuristic won't be able to read the CSV file. 
    """
    
    """ Testing skills
    """
    def test_skills_H(self):
        dict_1 = {'1': 1, '2': 1}
        dict_2 = {'1': 2, '3': 1}

        result = skills.Heuristic(dict_1, dict_2)
        self.assertEqual(result, (1*2)/((2*1)+(1*1)))

    def test_skills_H_noSkillsO(self):
        dict_1 = {'1': 1, '2': 1}
        dict_2 = {}

        result = skills.Heuristic(dict_1, dict_2)
        self.assertEqual(result, 0)

    def test_skills_H_noSkillsU(self):
        dict_1 = {}
        dict_2 = {'1': 1, '2': 1}

        result = skills.Heuristic(dict_1, dict_2)
        self.assertEqual(result, 0)

    def test_skills_H_noSkillsUO(self):
        dict_1 = {}
        dict_2 = {}

        result = skills.Heuristic(dict_1, dict_2)
        self.assertEqual(result, 0)

    """ Testing languages
    """
    def test_languages_H(self):
        list1 = ['1', '2']
        list2 = ['1', '3', '4']

        result = languages.Heuristic(list1, list2)
        self.assertEqual(result, 1/3)

    def test_languages_H_noSkillsU(self):
        list1 = []
        list2 = ['1', '3', '4']

        result = languages.Heuristic(list1, list2)
        self.assertEqual(result, 0)
    
    def test_languages_H_noSkillsO(self):
        list1 = ['1', '3', '4']
        list2 = []

        result = languages.Heuristic(list1, list2)
        self.assertEqual(result, 0)

    def test_languages_H_noSkillsOU(self):
        list1 = []
        list2 = []

        result = languages.Heuristic(list1, list2)
        self.assertEqual(result, 0)

    """ Testing distances
    """
    def test_rawDistance_noGmap(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # Marseille
        offerLocation = {'coordinates': {'latitude': 43.2961743, 'longitude': 5.3699525}, 'country': "France"}

        result, useGmap = distance.RawDistance(userLocation['coordinates'], offerLocation['coordinates'])

        self.assertTrue((660 < result < 700) and (not useGmap))

    def test_rawDistance_Gmap(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # Colombes
        offerLocation = {'coordinates': {'latitude': 48.9220615, 'longitude': 2.2533313}, 'country': "France"}

        result, useGmap = distance.RawDistance(userLocation['coordinates'], offerLocation['coordinates'])
        self.assertTrue((8 < result < 10) and (useGmap))

    def test_distance_H_InsideCountryGmap(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # Colombes
        offerLocation = {'coordinates': {'latitude': 48.9220615, 'longitude': 2.2533313}, 'country': "France"}

        result = distance.Heuristic(userLocation, offerLocation)

        if(distance.USE_GMAP == "True"):
            result = result['gmapH']['transit']
        else:
            result = result['insideCountry']

        self.assertIsNotNone(result)

    def test_distance_H_InsideCountry(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # Marseille
        offerLocation = {'coordinates': {'latitude': 43.2961743, 'longitude': 5.3699525}, 'country': "France"}

        result = distance.Heuristic(userLocation, offerLocation)
        result = result['insideCountry']

        self.assertIsNotNone(result)
    
    def test_distance_H_countryH(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # London
        offerLocation = {'coordinates': {'latitude': 51.5073219, 'longitude': -0.1276474}, 'country': "London"}

        result = distance.Heuristic(userLocation, offerLocation)
        result = result['countryH']

        self.assertIsNotNone(result)

    def test_distance_H_countryH_FalseCountry(self):
        # Paris
        userLocation = {'coordinates': {'latitude': 48.866667, 'longitude': 2.333333}, 'country': "France"}

        # London
        offerLocation = {'coordinates': {'latitude': 51.5073219, 'longitude': -0.1276474}, 'country': "ZZZZ"}

        result = distance.Heuristic(userLocation, offerLocation)
        result = result['countryH']

        self.assertEqual(result, 0)
    
    def test_distance_H_no_userL(self):
        # London
        offerLocation = {'coordinates': {'latitude': 51.5073219, 'longitude': -0.1276474}, 'country': "London"}

        result = distance.Heuristic({}, offerLocation)
        result = result['countryH']

        self.assertIsNone(result)
    
    def test_distance_H_no_offerL(self):
        # London
        userLocation = {'coordinates': {'latitude': 51.5073219, 'longitude': -0.1276474}, 'country': "London"}

        result = distance.Heuristic(userLocation, {})
        result = result['countryH']

        self.assertIsNone(result)
    
    def test_distance_H_no_offer_user_L(self):

        result = distance.Heuristic({}, {})
        result = result['countryH']

        self.assertIsNone(result)






    

if __name__ == '__main__':
    unittest.main()
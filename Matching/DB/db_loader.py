from itertools import count
from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData, select
from dotenv import load_dotenv
from sqlalchemy.sql.expression import null

from DB.model.user import User # pylint: disable=import-error
from DB.model.offer import Offer # pylint: disable=import-error

import os
load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
url = CONNECTION_STRING
db = create_engine(url)
meta = MetaData(db)

def load_user():
    """ Load users from DB 

    For each user, get its skills

    :return: listUsers, list of user objects
    """
    try:
        listUsers = list()

        with db.connect() as conn:
            user = Table('users', meta, autoload=True, autoload_with=db)

            skills_user = Table('users_skills', meta, autoload=True, autoload_with=db)

            query = select([user])
            ResultProxy = conn.execute(query)
            users = ResultProxy.fetchall()

            for unique_user in users:
                if('country' in unique_user.localities):
                    user_uuid = unique_user.uuid
                    skills_query = select(skills_user).filter_by(user_id = user_uuid)
                    ResultProxy = conn.execute(skills_query)
                    skills = ResultProxy.fetchall()
                    skill_ids = []
                    for skill in skills:
                        skill_ids.append(skill.skill_id)
                    listUsers.append(User(user_uuid, skill_ids, {'coordinates':{"longitude": unique_user.longitude, "latitude": unique_user.latitude}, "country": unique_user.localities['country']}, unique_user.languages))

        return listUsers
    except:
        return []

def load_offer(offer_id):
    """ Load an offer based on an id

    :param: offer_id

    :return: offer object
    """
    try:
        offer = None
        with db.connect() as conn:
            offers = Table('offers', meta, autoload=True, autoload_with=db)

            offers_skills = Table('offers_skills', meta, autoload=True, autoload_with=db)
            query = select(offers).filter_by(uuid=offer_id)
            ResultProxy = conn.execute(query)
            unique_offer = ResultProxy.fetchall()[0]
            if('country' in unique_offer.localities):
                skills_query = select(offers_skills).filter_by(offer_id = offer_id)
                ResultProxy = conn.execute(skills_query)
                skills = ResultProxy.fetchall()
                skills_ids = []
                for skill in skills:
                    skills_ids.append(skill.skill_id)
                
                offer = Offer(offer_id, skills_ids, {'coordinates':{"longitude": unique_offer.longitude, "latitude": unique_offer.latitude}, "country": unique_offer.localities['country']}, unique_offer.languages)
        return offer
    except:
        return None
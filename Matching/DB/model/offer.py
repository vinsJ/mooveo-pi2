class Offer():
    """ Offer model
    """
    def __init__(self, id: str, skills_ids: dict(), location: dict(), languages: list):
        self.id = id
        self.skills = dict(zip(skills_ids, [1]*len(skills_ids)))
        self.location = location
        self.languages = languages
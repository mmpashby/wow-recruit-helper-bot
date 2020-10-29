import requests as r

class CharactersList:
    def __init__(self):
        self.api_url = "https://raider.io/api/v1"
    
    def __str__(self):
        return "Characters List Object..."
    
    def get_char(self, **kwargs):
        """Get Single Character from passed kwargs."""  
        params = [kwargs['player'],
                  kwargs['region'],
                  kwargs['realm']
        ]
        rqs = (
            f'{self.api_url}/characters/profile?region={params[1].lower()}'
            f'&realm={params[2].lower()}&name={params[0].lower()}'
            f'&fields=gear%2Cmythic_plus_scores_by_season%3Acurrent'
        )
        characters = r.get(rqs)
        return characters.status_code, characters.json()
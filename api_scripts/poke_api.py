from random import randint
from math import sqrt, ceil
from icecream import ic
from pokebase import APIResource, move as poke_move, APIMetadata

class Pokemon_info():

    def __init__(self) -> None:
        self.pokemon_info : dict = {}
        self.move_set : dict = {}
        self.lvl_base_stat: dict = {}

        self.random_values : dict = {}
        self.hp_dv : int = 0

    def normalise(self, pokemon: APIResource) -> dict:
        """
        Function creates a pokemon inforation dictionary. Containing important pokemon
        information.

        Paramaters
        ----------
        pokemon : APIResource
            This is the pokemon data that was retreived from the API
        """
        self.pokemon_info['Name'] = pokemon.name

        pokemon_stat = {}
        base_stat: APIMetadata

        for base_stat in pokemon.stats:
            pokemon_stat[base_stat.stat.name] = base_stat.base_stat
            # pokemon_stat[pokemon.stats.0.stat.name] = pokemon.stats.0.base_stat

        # Calculating roughly the actauly stat of pokemon base of the lvl
        self.pokemon_info['stats'] = pokemon_stat

        # Retrieving Type data
        # There can only be two types on a pokemon
        self.pokemon_info['Type1'] = pokemon.types[0].type.name
        try:
            self.pokemon_info['Type2'] = pokemon.types[1].type.name
        except IndexError as e:
            print(f"{e}: Pokemon doesn't have a second type")

    def stat_calculation(self, lvl: int) -> tuple[dict, dict]:
        """
        Returns dictionary of modifyed base stat, based on the lvl user has gdvin
        This will be random each time, due to the nature of Effort Value (EV) and Determinant Value (DV)

        Paramaters
        ----------
        lvl : int
            User input level of there pokemon

        Creates
        ------
        lvl_base_stat : dict
            Close to actual lvl base_stat based on random DV and EV
        random_values : dict
            The numbers that the base stats where updated from. The order -> [DV, EV]
        """

        # -> Should be returned for the PDF purpouse (LATER THING WE WILL NEED TO PROCESS)
        # -> GEN 1 and GEN 2 Calculations only
        for key in self.pokemon_info['stats']:
            # We need to calculate other stats dv to get hp's dv
            if key != 'hp':
                # In gen 1 & 2 pokemon (Sp.Atk & Sp.Def share the same DV and EV)
                # If spt.atk or spt.def is already calcualted then resuse it
                if (key == 'special-attack' or key == 'special-defense') and ('special-attack' in self.random_values or 'special-defense' in self.random_values):
                    try:
                        self.stat_formulat(key, self.pokemon_info['stats'][key], lvl, self.random_values['special-defense'][0], self.random_values['special-defense'][1])
                    except KeyError:
                        self.stat_formulat(key, self.pokemon_info['stats'][key], lvl, self.random_values['special-attack'][0], self.random_values['special-attack'][1])

                else:
                    self.stat_formulat(key, self.pokemon_info['stats'][key], lvl, randint(0,15), randint(0,255))

                # If DV is odd, adds to the DV for the HP calculation (Gen 1 and Gen 2)
                if self.random_values[key][0] % 2:
                    match key:
                        case "attack":
                            self.hp_dv += 8
                        case "defense":
                            self.hp_dv += 4
                        case "speed":
                            self.hp_dv += 2
                        case "special-attack":
                            self.hp_dv += 1

        # Calcualte the Hp's new val
        self.stat_formulat('hp', self.pokemon_info['stats']['hp'], lvl, self.hp_dv, randint(0,255))

    def stat_formulat(self, n_stat: str, stat: int, lvl: int, dv: int, ev: int):
        """
        Formula for the a stat calcuation Gen 1 and 2

        Paramaters
        ----------
        n_stat : str
            Name of the stat your changing
        stat : int
            Base stat number
        lvl : int
            Level of the pokemon you want to see the stat of
        dv : int
            Determinant Value, range(0,15)
        EV : int
            Effort Value, range(0,255)
        """
        self.random_values[n_stat] = [dv, ev]

        dv_cal : int = (stat + dv)*2
        ev_cal : float = ceil(sqrt(ev))/4

        # If Hp you +lvl and +10, else +5
        if n_stat == 'hp':
            self.lvl_base_stat[n_stat] = int((((dv_cal + ev_cal)*lvl)/100))+lvl+10
        else:
            self.lvl_base_stat[n_stat] = int((((dv_cal + ev_cal)*lvl)/100))+5

    def pokemon_move(self, name: str) -> None:
        """
        Retrieves, extracts, added to dictionary for each of the 6 moves there is on pokemon

        Paramaters
        ----------
        name : str
            Name of the move
        """
        move_stat = {}
        move = poke_move(name)

        # Retrievein data that we need
        move['Category'] = move.damage_class.name
        move_stat['Accuracy'] = move.accuracy
        move_stat['Power'] = move.power
        move_stat['PP'] = move.pp
        move_stat['Priority'] = move.priority
        move_stat['Type'] = move.type.name

        # Aligment might be None
        move_stat['Effect'] = move.ailgmnet.name
        move_stat['Effect_chance'] = move.ailgmnet.ailgmnet_chance

        self.move_set[name] = move_stat

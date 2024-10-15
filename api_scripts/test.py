import unittest
import poke_api as poke
from icecream import ic
from pokebase import pokemon

class pokemon_test(unittest.TestCase):

    def setUp(self) -> None:
        self.name : str = 'pikachu'
        self.raw_pokemon_data = pokemon(self.name)
        self.pikachu = poke.Pokemon_info()

    def api_retrieve(self) -> None:
        self.pikachu.normalise(self.raw_pokemon_data)

        ic(self.pikachu.pokemon_info)

    def cal_stats(self) -> None:
        self.pikachu.normalise(self.raw_pokemon_data)

        self.pikachu.stat_calculation(81)
        ic(self.pikachu.lvl_base_stat)
        ic(self.pikachu.random_values)
    
    def moves_retrieve(self) -> None:
        self.pikachu.normalise(self.raw_pokemon_data)

        ic(self.get_moves('thunder'))


if __name__ == '__main__':
    unittest.main()

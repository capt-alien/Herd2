#pytest to test Virus
import pytest
import io
import sys
import virus





def test_virus():
    #     Athena = superheroes.Hero("Athena")
    hiv = virus.Virus("HIV", .8, .3)
    assert hiv.name == 'HIV'
    assert hiv.mortality_rate == .8
    assert hiv.reproduction_rate ==.3

# self.name = name
# self.mortality_rate = mortaility_rate
# self.reproduction_rate = reproduction_rate

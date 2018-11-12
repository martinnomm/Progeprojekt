from random import randint
class Offensive_Spell:
   def __init__(self, mana_cost, type, damg):

       self.mana_cost = mana_cost
       self.type = type
       self.damg = damg

class Defensive_Spell:
    def __init__(self, mana_cost, type, effect):

        self.mana_cost = mana_cost
        self.type = type
        self.effect = effect
#panen prg dmg sama, mis weaponitel

class Fireball(Offensive_Spell):
    def __init__(self,mana_cost = 20, type = 'fire', damg = [1,6]):
        super().__init__(mana_cost, type, damg)
        self.attribute = 'burn'

class Thunderbolt(Offensive_Spell):
    def __init__(self, mana_cost = 20, type = 'electric', damg = [1,6]):
        super().__init__(mana_cost,type,damg)
        self.attribute = 'paralyze'
class Iceshard(Offensive_Spell):
    def __init__(self, mana_cost = 20, type = 'ice', damg = [1,6]):
        super().__init__(mana_cost,type,damg)
        self.attribute = 'freeze'
class Heal(Defensive_Spell):
    def __init__(self, mana_cost = 25, type = 'self-heal', effect = 'restore hp' ):
        super().__init__(mana_cost,type,effect)
        self.heal = randint(4,10)

class HealStatus(Defensive_Spell):
    def __init__(self, mana_cost = 15, type = 'self-heal', effect = 'heal status condition'):
        super().__init__(mana_cost,type,effect)







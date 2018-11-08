class Offensive_Spell:
   def __init__(self, mana_cost, type, dmg):

       self.mana_cost = mana_cost
       self.type = type
       self.dmg = dmg

class Defensive_Spell:
    def __init__(self, mana_cost, type, effect):

        self.mana_cost = mana_cost
        self.type = type
        self.effect = effect
#panen prg dmg sama, mis weaponitel

class Fireball(Offensive_Spell):
    def __init__(self,mana_cost = 20, type = 'fire', dmg = [1,6]):
        super().__init__(mana_cost, type, dmg)

class Thunderbolt(Offensive_Spell):
    def __init__(self, mana_cost = 20, type = 'electric', dmg = [1,6]):
        super().__init__(mana_cost,type,dmg)

class Iceshard(Offensive_Spell):
    def __init__(self, mana_cost = 20, type = 'ice', dmg = [1,6]):
        super().__init__(mana_cost,type,dmg)

class Heal(Defensive_Spell):
    def __init__(self, mana_cost = 25, type = 'self-heal', effect = 'restore hp' ):
        super().__init__(mana_cost,type,effect)

class HealStatus(Defensive_Spell):
    def __init__(self, mana_cost = 15, type = 'self-heal', effect = 'heal status condition'):
        super().__init__(mana_cost,type,effect)





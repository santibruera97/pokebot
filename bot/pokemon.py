from sqlalchemy import Column, String, Integer,ForeignKey

from base import Base


class Pokemon(Base):
    __tablename__ = 'pokemons'

    pokemon_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    front_sprite = Column(String)
    back_sprite = Column(String)


    def __init__(self, name,hp,attack,defense,special_attack,special_defense,speed,front_sprite,back_sprite,user_id):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.front_sprite = front_sprite
        self.back_sprite = back_sprite
        self.user_id = user_id

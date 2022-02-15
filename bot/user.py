from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_discord_id = Column(String)
    ultraballs = Column(Integer)
    superballs = Column(Integer)
    masterballs = Column(Integer)
    pokemons = relationship("Pokemon")

    def __init__(self, user_discord_id,ultraballs,superballs,masterballs,pokemons):
        self.user_discord_id = user_discord_id
        self.ultraballs = ultraballs
        self.superballs = superballs
        self.masterballs = masterballs
        self.pokemons = pokemons
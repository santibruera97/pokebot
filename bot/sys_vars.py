from sqlalchemy import Column, String, Integer,DateTime
from sqlalchemy.orm import relationship
import datetime

from base import Base


class SystemVars(Base):
    __tablename__ = 'sys_vars'

    id_var = Column(Integer, primary_key=True)
    var_name = Column(String)
    var_value = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    guild_id = Column(String,unique=True)

    def __init__(self, var_name,var_value,guild_id):
        self.var_name = var_name
        self.var_value = var_value
        self.guild_id = guild_id
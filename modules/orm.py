"""
    This module provides implementation of ORM technology for database interactions.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Creating connection to database
engine = create_engine('sqlite:///vanguard.db')

Base = declarative_base()

class Card(Base):
    """
    Class representing a 'Cardfight!! Vanguard' Card

    Attributes:
        __tablename__ (str): Name of the database table.
        __table_args__ (dict): Parameters of the database table.
        name (str): Name of the character.

    Methods:
        __repr__ -- returns string representation of object. In this case only name attribute.
    """
    __tablename__ = 'Cards'
    __table_args__ = {'extend_existing': True}

    name = Column(String(255), primary_key=True, nullable=False)
    grade = Column(Integer, nullable=False)
    power = Column(Integer, nullable=False)
    critical = Column(Integer, nullable=False)
    shield = Column(Integer)

    clan_name = Column(String(50), ForeignKey('Clans.name'), nullable=False)
    clan = relationship('Clan', backref='cards')

    def __repr__(self):
        return f'{self.name}'


class Clan(Base):
    """
    Class representing a 'Cardfight!! Vanguard' Clan

    Attributes:
        __tablename__ (str): Name of the database table.
         __table_args__ (dict): Parameters of the database table.
        name (str): Name of the clan.
        imaginary_gift_name (str): Name of imaginary gift associated with clan (Foreign Key).
        imaginary_gift (Relationship): Relationship between ImaginaryGift class and Clan class.
        nation_name (str): Name of nation associated with clan (Foreign Key).
        nation (Relationship): Relationship between Nation class and Clan class.
    """
    __tablename__ = 'Clans'
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), primary_key=True, nullable=False)
    imaginary_gift_name = Column(String(50), ForeignKey(
        'ImaginaryGifts.name'), nullable=False)
    imaginary_gift = relationship('ImaginaryGift', backref='clans')
    nation_name = Column(String(50), ForeignKey('Nations.name'), nullable=False)
    nation = relationship('Nation', backref='clans')


class ImaginaryGift(Base):
    """
    Class representing a 'Cardfight!! Vanguard' Imaginary Gift.
        
    Attributes:
        __tablename__ (str): Name of the database table.
        __table_args__ (dict): Parameters of the database table.
        name (str): Name of the Imaginary Gift.
    """
    __tablename__ = 'ImaginaryGifts'
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), primary_key=True, nullable=False)
    
class CardInstance(Base):
    """
    Class representing a 'Cardfight!! Vanguard' Card instance inside of database.
    
    Attributes:
        __tablename__ (str): Name of the database table.
        __table_args__ (dict): Parameters of the database table.
        id (int): auto-incremented id for identifying exact copy of card.
        card_name (str): Name of the card associated with exact card instance.
        rarity (str): Rarity of card instance.
        card (Relationship): Relationship between Card class and CardInstance class.
    """
    __tablename__ = 'CardInstances'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    card_name = Column(String(255), ForeignKey('Cards.name'), nullable=False)
    rarity = Column(String(3), nullable=False)
    card = relationship('Card', backref='instances')
    
    def __repr__(self):
        return f'{self.card_id};{self.rarity}'
    
class Nation(Base):
    """
    Class representing a 'Cardfight!! Vanguard' Nation.
        
    Attributes:
        __tablename__ (str): Name of the database table.
        __table_args__ (dict): Parameters of the database table.
        name (str): Name of the nation.
    """
    __tablename__ = 'Nations'
    __table_args__ = {'extend_existing': True}
    
    name = Column(String(50), primary_key=True, nullable=False)
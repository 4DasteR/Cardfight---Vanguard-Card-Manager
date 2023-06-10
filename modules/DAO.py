"""
    This module is responsible for providing implementation of Database Access Object (DAO).
"""
from modules.orm import Card, Clan, ImaginaryGift, engine, CardInstance, Nation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update, delete, select, not_, func
from sqlalchemy.exc import SQLAlchemyError

class DAO:
    """
    Class representing Database Access Object.
    
    Attributes:
        session (Session): session object which allows for interacting with database.
        
    Methods:
        add_card (bool) -- adds card to the database. If there exists already one copy of the card just its instance will be added.\n
        get_all_cards (List[Card]) -- returns list of all cards in database (not counting copies).\n
        get_grade_cards (List[Card]) -- returns list of all cards in database (not counting copies) for specific grade. If grade is 'All' it will return list of all cards in database.\n 
        get_clan_cards (List[Card]) -- returns list of all cards in database (not counting copies) for specific clan. If clan is'All Clans' it will return list of all cards in database.\n
        get_clan_grade_cards (List[Card]) -- returns list of all cards in database (not counting copies) for specific clan and grade. Follows the same constraints as two above methods.\n
        get_card_rarities (str) -- resturns string representing all distinct rarities for all copies of a card with specified name.\n
        get_card_instances (List[CardInstance]) -- returns list of all instances of a card with specified name.\n
        get_card_count (int) -- returns number of instances of a card with specified name.\n
        get_card_grades (List[Tuple[int]]) -- returns list of tuples containing grades for all cards in database.\n
        get_cards_grades_count (List[Tuple[int]]) -- returns list of tuples containing grades and number of cards for specific grade.\n
        get_cards_clan_count (List[Tuple[int]]) -- returns list of tuples containing clans and number of cards for specific clan.\n
        update_card (bool) -- updates card object, if after update no card with same name exists new card is created.\n
        delete_card (bool) -- deletes specific instance of a card, returns True if there was no Exception.\n
        __delete_cards__ (bool) -- deletes all cards that don't have any distances, returns True if there was no Exception.\n
        add_clan (bool) -- adds new clan to database.\n
        get_all_clans (List[Clan]) -- returns all clans in databse.\n
        get_clans_with_cards (List[Clan]) -- returns clans for which there exisits at least one card.\n
        add_imaginary_gift (bool) -- adds new imaginary gift to database.\n
        add_nation (bool) -- adds new nation to database.
    """
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def add_card(self, name: str, grade: int, power: int, critical: int, shield: int | None, clan_name: str, card_rarity: str):
        try:
            existing_card = self.session.query(Card).filter_by(name=name).first()
            if not existing_card: 
                self.session.add(Card(name=name, grade=grade, power=power, critical=critical, shield=shield, clan_name=clan_name))
            self.session.add(CardInstance(card_name=name, rarity=card_rarity))
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def get_all_cards(self):
        try:
            return self.session.query(Card).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_grade_cards(self, grade: str):
        try:
            if grade != 'All':
                return self.session.query(Card).filter(Card.grade == int(grade)).all()
            else:
                return self.session.query(Card).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_clan_cards(self, clan: str):
        try:
            if clan != 'All Clans':
                return self.session.query(Card).filter(Card.clan_name == clan).all()
            else:
                return self.get_all_cards()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_clan_grade_cards(self, clan: str, grade: str):
        try:
            if clan != 'All Clans':
                query = self.session.query(Card).filter(Card.clan_name == clan)
                if grade != 'All':
                    return query.filter(Card.grade == int(grade)).all()
                else:
                    return query.all()
            else:
                return self.get_grade_cards(grade)
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_card_rarities(self, name: str):
        rarities = []
        try:
            for _, rarity in (
                self.session.query(Card, CardInstance.rarity).join(CardInstance)
                .filter(Card.name == CardInstance.card_name)
                .filter(Card.name == name)
                .distinct()):
                rarities.append(rarity)
        except SQLAlchemyError: 
            self.session.rollback()
        return ', '.join(rarities)
    
    def get_card_instances(self, name: str):
        instances = []
        try:
            for _, instance in (
                self.session.query(Card, CardInstance).join(CardInstance)
                .filter(Card.name == CardInstance.card_name)
                .filter(Card.name == name)
                .distinct()):
                instances.append(instance)
        except SQLAlchemyError: 
            self.session.rollback()
        return instances
    
    def get_card_count(self, name: str):
        try:
            return self.session.query(Card).join(CardInstance).filter(Card.name == CardInstance.card_name).filter(Card.name == name).count()
        except SQLAlchemyError:
            self.session.rollback()
            return 0
        
    def get_card_grades(self):
        try:
            return self.session.query(Card.grade).distinct().order_by(Card.grade).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_cards_grades_count(self):
        try:
            return self.session.query(Card.grade, func.count()).join(CardInstance).group_by(Card.grade).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_cards_clan_count(self):
        try:
            return self.session.query(Card.clan_name, func.count()).join(CardInstance).group_by(Card.clan_name).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def update_card(self, instance_id: int, name: str, grade: int, power: int, critical: int, shield: int | None, clan_name: str, card_rarity: str):
        try:
            if self.session.query(CardInstance).filter(CardInstance.id == instance_id).first() == None: return False
            stmt = update(CardInstance).where(CardInstance.id == instance_id).values(card_name=name, rarity=card_rarity)
            self.session.execute(stmt)
            
            if self.get_card_count(name) == 0:
                self.session.add(Card(name=name, grade=grade, power=power, critical=critical, shield=shield, clan_name=clan_name))
                
            elif self.get_card_count(name) == 1:
                stmt = update(Card).where(Card.name == name).values(grade=grade, power=power, critical=critical, shield=shield, clan_name=clan_name)
                self.session.execute(stmt)
                
            self.__delete_cards__()
            
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False
        
    def delete_card(self, instance_id: int):
        try:
            stmt = delete(CardInstance).where(CardInstance.id == instance_id)
            self.session.execute(stmt)
            self.__delete_cards__()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False
        
    def __delete_cards__(self):
        try:
            subquery = select(CardInstance.card_name.distinct()).subquery()
            query = select(Card.name).where(not_(Card.name.in_(select(subquery))))
            card_without_instances = self.session.execute(query).fetchall()
            
            for card in card_without_instances:
                stmt = delete(Card).where(Card.name == card[0])
                self.session.execute(stmt)
                
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def add_clan(self, name: str, imaginary_gift_name: str, nation: str):
        session = sessionmaker(bind=engine)()
        try:
            session.add(Clan(name=name, imaginary_gift_name=imaginary_gift_name, nation_name=nation))
            session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False
        
    def get_all_clans(self):
        try:
            return self.session.query(Clan).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []
        
    def get_clans_with_cards(self):
        try:
            return self.session.query(Clan).join(Card).all()
        except SQLAlchemyError:
            self.session.rollback()
            return []

    def add_imaginary_gift(self, name: str):
        session = sessionmaker(bind=engine)()
        try:
            session.add(ImaginaryGift(name=name))
            session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def add_nation(self, name: str):
        session = sessionmaker(bind=engine)()
        try:
            session.add(Nation(name=name))
            session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False
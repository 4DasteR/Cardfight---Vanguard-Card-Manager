"""
    This module is used for loading data from specified xlsx file, filling db with necessary data, and for loading and saving backups.
"""
import pandas as pd
import shutil
import os

class Loader():
    """
        Class responsible for loading data from specified xlsx file and filling db with necessary data
        
        Attributes:
            dao (DAO): Database Access Object.
            
        Methods:
            load_cards_from_xlsx -- saves cards loaded from xlsx file using pandas dataframe to database using DAO object.\n
            load_basic_data (bool) -- saves to database predefined values necessary for any card from 'Cardfight!! Vanguard'
    """
    def __init__(self, dao):
        self.dao = dao
        
    def load_cards_from_xlsx(self, path):
        df = pd.read_excel(path, sheet_name='Wszystkie karty')
        df = df.dropna(subset=['Grade', 'Power'])
        df.fillna('', inplace=True)
        with open('c.csv', 'w', encoding='utf-8') as file:
            for v, card in df.iterrows():
                print(f"{card['Nazwa']};{card['Klan']};{int(card['Grade'])};{int(card['Power'])};{card['Defence']};{card['Rarity']}", file=file)
                if card['Defence'] == '': shield = None
                else: shield = card['Defence']
                self.dao.add_card(name=card['Nazwa'], power=int(card['Power']), critical=1, grade=int(card['Grade']), clan_name=card['Klan'], card_rarity=card['Rarity'], shield=shield)
                
        pass
        
    def load_basic_data(self):
        try:
            [self.dao.add_nation(nation) for nation in ['United Sanctuary', 'Dragon Empire', 'Dark Zone', 'Star Gate', 'Magallanica', 'Zoo']]
            [self.dao.add_imaginary_gift(gift) for gift in ['Accel', 'Protect', 'Force']]
            self.dao.add_clan('Royal Paladin', 'Force', 'United Sanctuary')
            self.dao.add_clan('Oracle Think Tank', 'Protect', 'United Sanctuary')
            self.dao.add_clan('Angel Feather', 'Protect', 'United Sanctuary')
            self.dao.add_clan('Shadow Paladin', 'Force', 'United Sanctuary')
            self.dao.add_clan('Gold Paladin', 'Accel', 'United Sanctuary')
            self.dao.add_clan('Genesis', 'Force', 'United Sanctuary')
            self.dao.add_clan('Kagero', 'Force', 'Dragon Empire')
            self.dao.add_clan('Nubatama', 'Protect', 'Dragon Empire')
            self.dao.add_clan('Tachikaze', 'Accel', 'Dragon Empire')
            self.dao.add_clan('Murakumo', 'Accel', 'Dragon Empire')
            self.dao.add_clan('Narukami', 'Accel', 'Dragon Empire')
            self.dao.add_clan('Nova Grappler', 'Accel', 'Star Gate')
            self.dao.add_clan('Dimension Police', 'Force', 'Star Gate')
            self.dao.add_clan('Link Joker', 'Force', 'Star Gate')
            self.dao.add_clan('Spike Brothers', 'Force', 'Dark Zone')
            self.dao.add_clan('Dark Irregulars', 'Protect', 'Dark Zone')
            self.dao.add_clan('Pale Moon', 'Accel', 'Dark Zone')
            self.dao.add_clan('Gear Chronicle', 'Force', 'Dark Zone')
            self.dao.add_clan('Granblue', 'Protect', 'Magallanica')
            self.dao.add_clan('Bermuda Triangle', 'Force', 'Magallanica')
            self.dao.add_clan('Aqua Force', 'Accel', 'Magallanica')
            self.dao.add_clan('Megacolony', 'Protect', 'Zoo')
            self.dao.add_clan('Great Nature', 'Accel', 'Zoo')
            self.dao.add_clan('Neo Nectar', 'Force', 'Zoo')
            return True
        except:
            return False
        
def save_backup():
    """
    This method is used for performing backup of database.
    """
    shutil.copyfile('vanguard.db', 'vanguard_bk.db')
    
def load_backup():
    """
    This method is used for loading backup of database.
    """
    if os.path.exists('vanguard_bk.db'):
        shutil.copyfile('vanguard_bk.db', 'vanguard.db')
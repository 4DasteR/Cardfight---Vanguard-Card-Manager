from modules.DAO import DAO
from modules.loader import load_backup
import tkinter as tk
from modules.gui import CardImageLabel, IMG_SIZE, OperationFrame, CenterFrame
from modules.orm import engine, Base, Card
from modules.handler import Handler
import os

class Application():
    """
    Main class of whole program. It is defacto the 'Cardfight!! Vanguard' Card manager itself
    
    Attributes:
        dao (DAO): Database Access Object.
        window (tk.Tk): tkinter window which houses all other GUI components.
        handler (Handler): handler object holding references to main three components of GUI of Application.
        current_card (Card): currently selected card.
        current_clan (Clan): currently selected clan or all clans.
        card_image_label (CardImageLabel): custom GUI component used to display image of current card.
        right_frame (OperationFrame): custom GUI component used to allow user to add, edit, delte and show plots related to current card or all cards. Also allows for performing a backup.
        center_frame (CenterFrame): custom GUI component used to display all informations about current card and allows for selecing new one with filtering options.
    """
    def __init__(self):
        self.dao: DAO = DAO()
        self.window: tk.Tk = tk.Tk()
        self.handler: Handler = Handler()
        self.window.title('Cardfight!! Vanguard Card Manager')
        self.window.resizable(False, False)
        self.current_card: Card = self.dao.get_all_cards()[0]
        self.current_clan: str = 'All Clans'
        
        image_height: int = IMG_SIZE['height'] #px
        
        #Left side content (Image)
        self.card_image_label = CardImageLabel(self.window, f"images/{self.current_card.name}.jpg")
        
        #Right side content (Options)
        self.right_frame = OperationFrame(self.window, width=300, height=image_height, dao=self.dao, current_card=self.current_card, handler=self.handler)
        
        #Main content
        self.center_frame = CenterFrame(self.window, 
                                        width=300, 
                                        height=image_height, 
                                        dao=self.dao, 
                                        current_card=self.current_card, 
                                        current_clan=self.current_clan, 
                                        handler=self.handler)
        
        self.handler.configure(self.card_image_label, self.center_frame, self.right_frame)
        
        self.card_image_label.pack(side=tk.LEFT)
        self.center_frame.pack(side=tk.LEFT, padx=10)
        self.right_frame.pack(side=tk.LEFT, padx=10)   
        
        self.window.mainloop()

if __name__ == "__main__":
    """
        Starting point of program. 
        If no database file is found it will attempt to load the backup file.
        Then it creates all metadata for db connection and starts the program by creating the Application object
    """
    if not os.path.exists('vanguard.db'):
        load_backup()
        
    Base.metadata.create_all(engine)
    Application()
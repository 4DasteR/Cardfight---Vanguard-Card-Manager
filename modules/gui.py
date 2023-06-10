"""
    This module is responsible for all main GUI components.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from modules.scrapper import Scrapper
from modules.DAO import DAO
from modules.loader import save_backup
from modules.handler import Handler
from modules.orm import Card
import modules.plots as plots
from PIL import Image, ImageTk
import os
from urllib.parse import quote
import re
from abc import ABC

IMG_SIZE = {'width': 412, 'height': 600}
BTN_WIDTH = 20

class CardImageLabel(tk.Label):
    """
    Class representing tkinter Label specifically designed to display image of currently selected card.
    Inherits from tk.Label
    
    Attributes:
        scrapper (Scrapper): scrapper object which will be used to download card image from the wiki.
        card_image (PhotoImage): image object holding an image of specific card.
        
    Methods:
        update_image -- updates image to the new one based on path to image file.\n
        load_image (Image) -- loads image object for specific path, if image file doesn't exist it will be downloaded from wiki using scrapper object. If no image was found the default image will be loaded.
    """
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.scrapper = Scrapper()
        resized_image = self.load_image(image_path).resize((IMG_SIZE['width'], IMG_SIZE['height']), Image.LANCZOS)
        self.card_image = ImageTk.PhotoImage(resized_image)
        self.configure(image=self.card_image)

    def update_image(self, path: str):
        new_image = ImageTk.PhotoImage(self.load_image(path).resize((IMG_SIZE['width'], IMG_SIZE['height']), Image.LANCZOS))
        self.configure(image=new_image)
        self.image = new_image

    def load_image(self, path: str):
        """
        Loads image object for specific path, if image file doesn't exist it will be downloaded from wiki using scrapper object. If no image was found the default image will be loaded.
        
        Args:
            path (str): path to image file
            
        Returns:
            Image: image corresponding to given path, or default image
        """
        image_path = path.replace('"', quote('"'))
        if not os.path.exists(image_path):
            scrapped = self.scrapper.extract_image(image_path.replace('.jpg', '').replace('images/', ''))
            if not scrapped:
                image_path = 'images/vanguardsleevelogo.png'
        return Image.open(image_path)

class OperationFrame(tk.Frame):
    """
    Class representing tkinter Frame specifically designed to allow user to perform operations, like adding, editing, deleting cards. Also creating plots and backup.
    Inherits from tk.Frame
    
    Attributes:
        dao (DAO): Database Access Object
        handler (Handler): handler object holding references to main three components of GUI of Application
        current_card (Card): card object representing currently selected card  
   """
    def __init__(self, parent, width=..., height=..., dao: DAO = None, current_card: Card = None, handler: Handler = None):
        super().__init__(parent, width=width, height=height, borderwidth=2)
        self.dao = dao
        self.handler = handler
        self.current_card = current_card
        card_add_button = tk.Button(self, text="Add new card", width=BTN_WIDTH)
        card_edit_button = tk.Button(self, text="Edit current card", width=BTN_WIDTH)
        card_delete_button = tk.Button(self, text="Delete current card", width=BTN_WIDTH)
        db_backup_button = tk.Button(self, text="Backup", width=BTN_WIDTH, background='#FFF3B0', foreground='#335C67')
        card_grade_count_button = tk.Button(self, text="Card Grades Distribution", width=BTN_WIDTH)
        card_clan_count_button = tk.Button(self, text="Card Clans Distribution", width=BTN_WIDTH)
        card_add_button.pack(side=tk.TOP)
        card_edit_button.pack(side=tk.TOP, pady=2)
        card_delete_button.pack(side=tk.TOP, pady=2)
        card_grade_count_button.pack(side=tk.TOP, pady=2)
        card_clan_count_button.pack(side=tk.TOP, pady=2)
        db_backup_button.pack(side=tk.TOP, pady=2)

        def open_add_card_window():
            AddNewCardWindow(self.master, width, 250, dao, handler)

        def open_edit_card_window():
            EditCurrentCardWindow(self.master, width, 275,dao, self.current_card, handler)

        def open_delete_card_window():
            DeleteCardWindow(self.master, width, 80, dao, self.current_card, handler)

        def card_grade_distribution():
            plots.card_grade_distribution(self.dao)

        def card_clan_distribution():
            plots.card_clan_distribution(self.dao)

        card_add_button.configure(command=open_add_card_window)
        card_edit_button.configure(command=open_edit_card_window)
        card_delete_button.configure(command=open_delete_card_window)
        db_backup_button.configure(command=save_backup)
        card_grade_count_button.configure(command=card_grade_distribution)
        card_clan_count_button.configure(command=card_clan_distribution)

class AddEditCardWindow(tk.Toplevel, ABC):
    """
    Abstract class representing tkinter TopLevel specifically designed to be inherited by either TopLevel for adding or editing card
    Inherits from tk.Toplevel and ABC
    
    Attributes:
        dao (DAO): Database Access Object.
        handler (Handler): handler object holding references to main three components of GUI of Application.
        main_frame (tk.Frame): frame holding content of the window.
        name_entry (tk.Entry): allows to input card's name, that name will be validated.
        grade_spinbox (tk.Spinbox): allows to select grade of a card from 0 to 5.
        power_spinbox (tk.Spinbox): allows to select power of a card in range from 1000 to 30000, with step of 1000.
        critical_spinbox (tk.Spinbox): allows to select critical of a card in range from 1 to 6.
        shield_spinbox (tk.Spinbox): allows to select shield of a card in range from 0 to 30000, with step of 1000; also supports values: 'None' and 'Sentinel'.
        clan_combobox (ttk.Combobox): allows to select clan of a card.
        rarity_combobox (ttk.Combobox): allows to select rarity of a card.
        action_card_button (tk.Button): button created as a 'pocket' to be programmed by inheriting classes. Disabled by default.
        error_label (tk.Label): label used for diplaying an error message.
    There are also labels provided for above input components for tkinter.
    """
    def __init__(self, parent, width=..., height=..., dao: DAO = ..., handler: Handler = ...):
        super().__init__(parent, width=width, height=height)
        self.dao = dao
        self.handler = handler
        self.geometry(f"{width}x{height}")
        self.main_frame = tk.Frame(self, width=width, height=height)
        self.main_frame.pack()
        self.resizable(False, False)

        # Name textbox and label
        self.name_label = tk.Label(self.main_frame, text='Name:')
        self.name_label.grid(row=0, column=0, sticky='E', pady=3)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, pady=3)

        # Grade numberbox and label
        self.grade_label = tk.Label(self.main_frame, text='Grade:')
        self.grade_label.grid(row=1, column=0, sticky='E', pady=3)
        self.grade_spinbox = tk.Spinbox(self.main_frame, from_=0, to=5)
        self.grade_spinbox.grid(row=1, column=1, pady=3)

        # Power numberbox and label
        self.power_label = tk.Label(self.main_frame, text='Power:')
        self.power_label.grid(row=2, column=0, sticky='E', pady=3)
        self.power_spinbox = tk.Spinbox(
            self.main_frame, from_=1000, to=30000, increment=1000)
        self.power_spinbox.grid(row=2, column=1, pady=3)

        # Critical numberbox and label
        self.critical_label = tk.Label(self.main_frame, text='Critical:')
        self.critical_label.grid(row=3, column=0, sticky='E', pady=3)
        self.critical_spinbox = tk.Spinbox(self.main_frame, from_=1, to=6)
        self.critical_spinbox.grid(row=3, column=1, pady=3)

        # Shield numberbox and label
        self.shield_label = tk.Label(self.main_frame, text='Shield:')
        self.shield_label.grid(row=4, column=0, sticky='E', pady=3)
        self.shield_spinbox = tk.Spinbox(self.main_frame, values=('None', 'Sentinel') + tuple(range(0, 30001, 1000)))
        self.shield_spinbox.grid(row=4, column=1, pady=3)

        # Clan combobox and label
        self.clan_label = tk.Label(self.main_frame, text='Clan:')
        self.clan_label.grid(row=5, column=0, sticky='E', pady=3)
        self.clan_combobox = ttk.Combobox(self.main_frame, values=[clan.name for clan in self.dao.get_all_clans()], state='readonly')
        self.clan_combobox.current(0)
        self.clan_combobox.grid(row=5, column=1, pady=3)

        # Rarity combobox and label
        self.rarity_label = tk.Label(self.main_frame, text='Rarity:')
        self.rarity_label.grid(row=6, column=0, sticky='E', pady=3)
        self.rarity_combobox = ttk.Combobox(self.main_frame, values=['C', 'R', 'RR', 'RRR', 'VR', 'SVR', 'SP', 'OR', 'IMR', 'Re', 'GR', 'SP', 'SGR'])
        self.rarity_combobox.current(0)
        self.rarity_combobox.grid(row=6, column=1, pady=3)

        self.action_card_button = tk.Button(self.main_frame, width=BTN_WIDTH, state='disabled')
        self.action_card_button.grid(row=7, column=0, sticky='E', pady=3)

        self.error_label = tk.Label(self.main_frame, fg="#8B0000")
        self.error_label.grid(row=9, column=0, pady=3)

        def validate_card_name():
            """
                Method used to validate cards name
            """
            # Get the entered value from the entry widget
            card_name = self.name_entry.get().strip()

            # Perform the validation using the regular expression
            pattern = r'^[\w\s"\',-]+$'
            if not re.match(pattern, card_name):
                self.action_card_button.config(state='disabled')
                return False

            self.action_card_button.config(state='normal')
            return True

        validate_cmd = self.main_frame.register(validate_card_name)
        self.name_entry.configure(validate='focusout', validatecommand=validate_cmd)

class AddNewCardWindow(AddEditCardWindow):
    """
    Class representing tkinter TopLevel specifically designed to enable adding of a new card
    Inherits from AddEditCardWindow
    
    Attributes:
        Inherited from parent class.
        action_card_button (tk.Button): button inherited from AddEditCardWindow class, configured to perform adding of a card on click.
        clear_card_button (tk.Button): allows to clean input components.
    """
    def __init__(self, parent, width=..., height=..., dao: DAO = ..., handler: Handler = ...):
        super().__init__(parent, width=width, height=height, dao=dao, handler=handler)

        self.title('Add New Card')
        self.action_card_button.configure(text="Add new card")
        clear_card_button = tk.Button(self.main_frame, text="Clear", width=BTN_WIDTH)
        clear_card_button.grid(row=7, column=1, pady=3)

        def clear_fields():
            self.name_entry.delete(0, 'end')
            self.grade_spinbox.delete(0, 'end')
            self.power_spinbox.delete(0, 'end')
            self.critical_spinbox.delete(0, 'end')
            self.shield_spinbox.delete(0, 'end')
            self.grade_spinbox.insert(0, 0)
            self.power_spinbox.insert(0, 1000)
            self.critical_spinbox.insert(0, 1)
            self.shield_spinbox.insert(0, 'None')
            self.clan_combobox.set(self.dao.get_all_clans()[0].name)
            self.rarity_combobox.set('C')
            self.action_card_button.configure(state='disabled')

        def add_card():
            shield = None if self.shield_spinbox.get() == "None" else self.shield_spinbox.get()
            added = self.dao.add_card(self.name_entry.get(), self.grade_spinbox.get(), self.power_spinbox.get(), self.critical_spinbox.get(), shield, self.clan_combobox.get(), self.rarity_combobox.get())
            if added:
                self.handler.center_frame.update_clans()
                self.handler.center_frame.update_cards()
                self.handler.center_frame.update_grades()
                self.destroy()
            else:
                self.error_label.configure(text='Cannot add card')

        clear_card_button.configure(command=clear_fields)
        self.action_card_button.configure(command=add_card)

class EditCurrentCardWindow(AddEditCardWindow):
    """
    Class representing tkinter TopLevel specifically designed to enable editing of a card
    Inherits from AddEditCardWindow
    
    Attributes:
        Inherited from parent class.
        current_card (Card): currently selected card.
        action_card_button (tk.Button): button inherited from AddEditCardWindow class, configured to perform editing of a card on click.
    """
    def __init__(self, parent, width=..., height=..., dao: DAO = ..., current_card: Card = None, handler: Handler = ...):
        super().__init__(parent, width=width, height=height, dao=dao, handler=handler)

        self.current_card = current_card
        self.title(f'Edit: {self.current_card.name}')

        self.action_card_button.configure(text='Edit card', state='normal')
        self.name_entry.insert(0, self.current_card.name)
        self.grade_spinbox.delete(0, tk.END)
        self.grade_spinbox.insert(0, self.current_card.grade)
        self.power_spinbox.delete(0, tk.END)
        self.power_spinbox.insert(0, self.current_card.power)
        self.critical_spinbox.delete(0, tk.END)
        self.critical_spinbox.insert(0, self.current_card.critical)
        self.shield_spinbox.delete(0, tk.END)
        self.shield_spinbox.insert(0, "None" if self.current_card.shield == None else self.current_card.shield)
        self.clan_combobox.set(self.current_card.clan.name)
        instances = self.dao.get_card_instances(self.current_card.name)
        copy_label = tk.Label(self.main_frame, text='Copy:')
        copy_label.grid(row=6, column=0, sticky='E', pady=3)
        copy_combobox = ttk.Combobox(self.main_frame, values=[f"ID: {instance.id}|{instance.rarity}" for instance in instances])
        copy_combobox.current(0)
        copy_combobox.grid(row=6, column=1, pady=3)
        current_rarity = copy_combobox.get().split('|', 1)[1]
        self.rarity_label.grid_forget()
        self.rarity_combobox.grid_forget()
        self.action_card_button.grid_forget()
        self.rarity_label.grid(row=7, column=0, sticky='E', pady=3)
        self.rarity_combobox.grid(row=7, column=1, pady=3)
        self.rarity_combobox.set(current_rarity)

        def update_rarity(event):
            current_rarity = copy_combobox.get().split('|', 1)[1]
            self.rarity_combobox.set(current_rarity)

        def edit_card():
            id = copy_combobox.get().split('|', 1)[0].replace('ID: ', '')
            shield = None if self.shield_spinbox.get() == "None" else self.shield_spinbox.get()
            edited = self.dao.update_card(id, self.name_entry.get(), self.grade_spinbox.get(), self.power_spinbox.get(), self.critical_spinbox.get(), shield, self.clan_combobox.get(), self.rarity_combobox.get())
            if edited:
                self.handler.center_frame.update_clans()
                self.handler.center_frame.update_cards()
                self.handler.center_frame.update_grades()
                self.destroy()
            else:
                self.error_label.configure(text='Cannot edit card')

        copy_combobox.bind("<<ComboboxSelected>>", update_rarity)
        self.action_card_button.grid(row=8, column=0, sticky='E', pady=3)
        self.action_card_button.configure(command=edit_card)

class DeleteCardWindow(tk.Toplevel):
    """
    Class representing tkinter TopLevel specifically designed to allow deleting exact instance of a card
    Inherits from tk.Toplevel
    
    Attributes:
        dao (DAO): Database Access Object
        handler (Handler): handler object holding references to main three components of GUI of Application.
        current_card (Card): currently selected card
        copy_combobox (ttk.Combobox): allows for selection of exact instance of a current card
        action_card_button (tk.Button): deletes card instance on click
        cancel_button (tk.Button): closes  this window
    """
    def __init__(self, parent, width=..., height=..., dao: DAO = ..., current_card: Card = None, handler: Handler = ...):
        super().__init__(parent, width=width, height=height)
        self.title('Delete Card')
        self.resizable(False, False)
        self.dao = dao
        self.handler = handler
        self.current_card = current_card
        self.geometry(f"{width}x{height}")
        main_frame = tk.Frame(self, width=width, height=height)
        main_frame.pack()

        name_label = tk.Label(main_frame, text=f'Name: {self.current_card}')
        name_label.pack(side=tk.TOP)
        copy_frame = tk.Frame(main_frame)
        copy_frame.pack(side=tk.TOP)

        instances = self.dao.get_card_instances(self.current_card.name)
        copy_label = tk.Label(copy_frame, text='Copy:')
        copy_label.grid(row=0, column=0, sticky='E', pady=3)
        copy_combobox = ttk.Combobox(copy_frame, values=[f"ID: {instance.id}|{instance.rarity}" for instance in instances])
        copy_combobox.current(0)
        copy_combobox.grid(row=0, column=1, pady=3)

        action_frame = tk.Frame(main_frame)
        action_frame.pack(side=tk.TOP)

        action_card_button = tk.Button(action_frame, width=BTN_WIDTH, text='Delete')
        action_card_button.grid(row=0, column=0, sticky='E', pady=3)

        cancel_button = tk.Button(action_frame, width=BTN_WIDTH, text='Close')
        cancel_button.grid(row=0, column=1, pady=3, padx=2)

        def close():
            self.destroy()

        def show_confirmation():
            result = messagebox.askyesno(
                "Confirmation", "Are you sure you want to delete this card instance?", icon="warning")
            if result == True:
                id = copy_combobox.get().split('|', 1)[0].replace('ID: ', '')
                self.dao.delete_card(int(id))
                self.handler.center_frame.update_clans()
                self.handler.center_frame.update_cards()
                self.handler.center_frame.update_grades()
                close()

        action_card_button.configure(command=show_confirmation)
        cancel_button.configure(command=close)

class CenterFrame(tk.Frame):
    """
    Class representing tkinter Frame specifically designed to hold all details and filering options of the card. Also allows to select card from list of all cards
    Inherits from tk.Frame
    
    Attributes:
        width (int): width of the frame.
        height (int): height of the frame.
        dao (DAO): Database Access Object.
        handler (Handler): handler object holding references to main three components of GUI of Application.
        current_card (Card): currently selected card.
        current_clan (Clan): currently selected clan or all clans.
        current_grade (str): currently selected grade or all grades.
        card_combobox (ttk.Combobox): allows to select current_card value.
        clan_combobox (ttk.Combobox): allows to select by which clan will card_combobox values filtered.
        grade_combobox (ttk.Combobox): allows to select by which grade will card_combobox values filtered.
        card_name_label (tk.Label): holds current card name value.
        card_grade_label (tk.Label): holds current card grade value.
        card_gift_frame (tk.Frame): holds current card imaginary gift value. Displayed only if card is grade 3.
        card_critical_label (tk.Label): holds current card critical value.
        card_shield_label (tk.Label): holds current card shield value. Not displayed for cards above and including grade 3.
        card_clan_label (tk.Label): holds current card clan value.
        card_nation_label (tk.Label): holds current card nation value.
        card_quantity_label (tk.Label): holds a number of all copies of current card
        card_rarity_label (tk.Label): holds all rarities of all copies of current card
        
    Methods:
        update_cards -- updates currently selected card to the one from card_combobox. Performes updates onto all tkinter components holding values about card and changes the image to the new card.\n
        update_clans -- updates currently selected clan to the one from clan_combobox. Changes values of card_combobox to display only cards from current_clan.\n
        update_grades -- updates currently selected grade to the one from grade_combobox. Changes values of card_combobox to display only cards of specified grade. Also works with clan filtering.
    """
    def __init__(self, parent, width: int = ..., height: int = ..., dao: DAO = ..., current_card: Card = ..., current_clan: str = ..., handler: Handler = ...):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.dao = dao
        self.current_card = current_card
        self.current_clan = current_clan
        self.current_grade = 'All'
        self.handler = handler
        # Selection of card
        cards = self.dao.get_all_cards()
        self.card_combobox = ttk.Combobox(self, width=40, state="readonly", values=[card.name for card in cards])
        self.card_combobox.pack(side=tk.TOP)
        self.card_combobox.current(0)

        self.clan_grade_frame = tk.Frame(self, width=40)
        self.clan_grade_frame.pack(side=tk.TOP, pady=3)

        # Selection of clans
        clans = ['All Clans'] + [clan.name for clan in self.dao.get_clans_with_cards()]
        self.clan_combobox = ttk.Combobox(self.clan_grade_frame, width=30, state="readonly", values=clans)
        self.clan_combobox.pack(side=tk.LEFT)
        self.clan_combobox.current(0)
        
        # Selection of grade
        grades = ['All'] + [grade[0] for grade in self.dao.get_card_grades()]
        self.grade_combobox = ttk.Combobox(self.clan_grade_frame, width=6, state='readonly', values=grades)
        self.grade_combobox.pack(side=tk.LEFT, padx=1)
        self.grade_combobox.current(0)
        
        # Name
        self.card_name_label = tk.Label(self, text=f"Name: {self.current_card.name}")
        # Grade
        self.card_grade_label = tk.Label(self, text=f"Grade: {self.current_card.grade}")
        # Imaginary gift
        self.card_gift_frame = tk.Frame(self)
        general_gift_icon = ImageTk.PhotoImage(Image.open("icons/gifts/Gift-icon.webp").resize((13,14)))
        self.general_gift_label = tk.Label(self.card_gift_frame, image=general_gift_icon)
        self.general_gift_label.image = general_gift_icon
        card_gift_icon = ImageTk.PhotoImage(file=f"icons/gifts/{self.current_card.clan.imaginary_gift.name}_icon.webp")
        self.card_gift_label = tk.Label(self.card_gift_frame, text=f"Imaginary Gift: ", compound=tk.RIGHT, image=card_gift_icon)
        self.card_gift_label.image = card_gift_icon
        # Power
        card_power_icon = ImageTk.PhotoImage(file="icons/Power_icon.webp")
        self.card_power_label = tk.Label(self, text=f"Power: {self.current_card.power}", compound=tk.LEFT, image=card_power_icon)
        self.card_power_label.image = card_power_icon
        # Critical
        card_critical_icon = ImageTk.PhotoImage(file="icons/Critical_icon.webp")
        self.card_critical_label = tk.Label(self, text=f"Critical: {self.current_card.critical}", compound=tk.LEFT, image=card_critical_icon)
        self.card_critical_label.image = card_critical_icon
        # Shield
        card_shield_icon = ImageTk.PhotoImage(file="icons/Shield_icon.webp")
        self.card_shield_label = tk.Label(self, text=f"Shield: {self.current_card.shield}", compound=tk.LEFT, image=card_shield_icon)
        self.card_shield_label.image = card_shield_icon
        # Clan
        card_clan_icon = ImageTk.PhotoImage(Image.open(f"icons/clans/Icon_{self.current_card.clan.name.replace(' ','')}.webp").resize((14, 14), Image.LANCZOS))
        self.card_clan_label = tk.Label(self, text=f"Clan: {self.current_card.clan.name}", compound=tk.LEFT, image=card_clan_icon)
        self.card_clan_label.image = card_clan_icon
        # Nation
        card_nation_icon = ImageTk.PhotoImage(file=f"icons/nations/{self.current_card.clan.nation.name}.webp")
        self.card_nation_label = tk.Label(self, text=f"Nation: {self.current_card.clan.nation.name}  ", compound=tk.RIGHT, image=card_nation_icon)
        self.card_nation_label.image = card_nation_icon
        # Quantity
        self.card_quanitiy_label = tk.Label(self, text=f"Quantity: {self.dao.get_card_count(self.current_card.name)}")
        # Rarity
        self.card_rarity_label = tk.Label(self, text=f"Rairties: {self.dao.get_card_rarities(self.current_card.name)}")

        self.card_name_label.pack(side=tk.TOP, anchor='w')
        self.card_grade_label.pack(side=tk.TOP, anchor='w')
        if self.current_card.grade == 3:
            self.card_gift_frame.pack(side=tk.TOP, anchor='w')
            self.general_gift_label.pack(side=tk.LEFT, anchor='w')
            self.card_gift_label.pack(side=tk.LEFT, anchor='w')
        self.card_power_label.pack(side=tk.TOP, anchor='w')
        self.card_critical_label.pack(side=tk.TOP, anchor='w')
        if self.current_card.shield is not None:
            self.card_shield_label.pack(side=tk.TOP, anchor='w')
        self.card_clan_label.pack(side=tk.TOP, anchor='w')
        self.card_nation_label.pack(side=tk.TOP, anchor='w')
        self.card_quanitiy_label.pack(side=tk.TOP, anchor='w')
        self.card_rarity_label.pack(side=tk.TOP, anchor='w')
        
        def card_selection(event):
            self.update_cards()
            
        def clan_selection(event):
            self.update_clans()
            
        def grade_selection(event):
            self.update_grades()

        self.card_combobox.bind("<<ComboboxSelected>>", card_selection)
        self.clan_combobox.bind("<<ComboboxSelected>>", clan_selection)
        self.grade_combobox.bind("<<ComboboxSelected>>", grade_selection)
        
    def update_cards(self):
        cards = self.dao.get_clan_grade_cards(self.current_clan, self.current_grade)
        self.card_combobox.configure(values=[card.name for card in cards])
        selected_index = self.card_combobox.current()
        self.current_card = cards[selected_index]
        self.handler.right_frame.current_card = self.current_card

        new_image_path = f"images/{self.current_card.name}.jpg"
        self.handler.card_image_label.update_image(new_image_path)

        self.card_name_label.configure(
            text=f"Name: {self.current_card.name}")
        self.card_grade_label.configure(
            text=f"Grade: {self.current_card.grade}")

        new_card_gift_icon = ImageTk.PhotoImage(file=f"icons/gifts/{self.current_card.clan.imaginary_gift.name}_icon.webp")
        self.card_gift_label.configure(image=new_card_gift_icon)
        self.card_gift_label.image = new_card_gift_icon
        if self.current_card.grade != 3:
            self.card_gift_frame.pack_forget()
        else:
            self.card_gift_frame.pack(side=tk.TOP, anchor='w')

        self.card_power_label.configure(text=f"Power: {self.current_card.power}")
        self.card_power_label.pack_forget()
        self.card_power_label.pack(side=tk.TOP, anchor='w')

        self.card_critical_label.configure(text=f"Critical: {self.current_card.critical}")
        self.card_critical_label.pack_forget()
        self.card_critical_label.pack(side=tk.TOP, anchor='w')

        self.card_shield_label.configure(text=f"Shield: {self.current_card.shield}")
        if self.current_card.shield is not None:
            self.card_shield_label.pack_forget()
            self.card_shield_label.pack(side=tk.TOP, anchor='w')
        else:
            self.card_shield_label.pack_forget()

        new_card_clan_icon = ImageTk.PhotoImage(Image.open(f"icons/clans/Icon_{self.current_card.clan.name.replace(' ','')}.webp").resize((14, 14), Image.LANCZOS))
        self.card_clan_label.configure(text=f"Clan: {self.current_card.clan.name}", image=new_card_clan_icon)
        self.card_clan_label.image = new_card_clan_icon

        self.card_clan_label.pack_forget()
        self.card_clan_label.pack(side=tk.TOP, anchor='w')

        new_card_nation_icon = ImageTk.PhotoImage(file=f"icons/nations/{self.current_card.clan.nation.name}.webp")
        self.card_nation_label.configure(text=f"Nation: {self.current_card.clan.nation.name}  ", image=new_card_nation_icon)
        self.card_nation_label.image = new_card_nation_icon

        self.card_nation_label.pack_forget()
        self.card_nation_label.pack(side=tk.TOP, anchor='w')

        self.card_quanitiy_label.configure(text=f"Quantity: {self.dao.get_card_count(self.current_card.name)}")
        self.card_quanitiy_label.pack_forget()
        self.card_quanitiy_label.pack(side=tk.TOP, anchor='w')

        self.card_rarity_label.configure(text=f"Rairties: {self.dao.get_card_rarities(self.current_card.name)}")
        self.card_rarity_label.pack_forget()
        self.card_rarity_label.pack(side=tk.TOP, anchor='w')

    def update_clans(self):
        clans = ['All Clans'] + [clan.name for clan in self.dao.get_clans_with_cards()]
        self.clan_combobox.configure(values=clans)
        selected_index = self.clan_combobox.current()
        self.current_clan = clans[selected_index]
        cards = self.dao.get_clan_grade_cards(self.current_clan, self.current_grade)
        self.card_combobox.configure(values=[card.name for card in cards])
        
    def update_grades(self):
        grades = ['All'] + [grade[0] for grade in self.dao.get_card_grades()]
        self.grade_combobox.configure(values=grades)
        selected_index = self.grade_combobox.current()
        self.current_grade = grades[selected_index]
        cards = self.dao.get_clan_grade_cards(self.current_clan, self.current_grade)
        self.card_combobox.configure(values=[card.name for card in cards])
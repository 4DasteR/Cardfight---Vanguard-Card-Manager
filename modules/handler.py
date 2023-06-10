"""
    This module is used to grant access to the Handler object.
"""

class Handler:
    """
    Class representing a handler object
    
    Attributes:
        card_image_label (CardImageLabel): custom GUI component used to display image of current card.
        right_frame (OperationFrame): custom GUI component used to allow user to add, edit, delte and show plots related to current card or all cards. Also allows for performing a backup.
        center_frame (CenterFrame): custom GUI component used to display all informations about current card and allows for selecing new one with filtering options.
    
    Methods:
        configure -- method necessary for handler to work. It overrides default None value of attributes with specified in arguments.
    """
    def __init__(self):
        self.card_image_label = None
        self.right_frame = None
        self.center_frame = None
        
    def configure(self, card_image_label, center_frame, right_frame):
        self.card_image_label = card_image_label
        self.right_frame = right_frame
        self.center_frame = center_frame
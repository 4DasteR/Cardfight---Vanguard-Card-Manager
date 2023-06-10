# 'Cardfight!! Vanguard' Card manager
This application is intended to be used as a manager for cards from cardgame 'Cardfight!! Vanguard'

## Installation
In order to use the program it is necessary to install required modules using [pip](https://pip.pypa.io/en/stable/) package manager.

```bash
pip install -r requirements.txt
```

## Starting the app
In order to start the program user needs to simply either run the ***main.py*** file from file explorer or run following command in command line:

- **Windows**
```bash
py main.py
```

- **Linux**
```bash
python3 main.py
```

## Feautures
***'Cardfight!! Vanguard'* Card manager** allows user to browse, add, delete and edit currently owned *'Cardfight!! Vanguard'* cards.
Modules from which the app is built are mostly located in [**modules**](./modules/) folder.
### Module breakdown
- **DAO.py**: This module is responsible for all database interactions. DAO means Database Access Object and it is used to implement mechanics for all interactions the program needs to have with database.
- **orm.py**: This module implements sqlalchemy logic of orm mapping for classes from database. It is closely tied with above DAO.py module.
- **plots.py**: This module is used to create and display following plots:
    + Cards distribution among their grades
    + Cards distribution among their classes
- **scrapper.py**: This module is responsible for web scrapping for images of cards from official [*'Cardfight!! Vanguard'* wiki](https://cardfight.fandom.com/wiki/'). It checks whether card is a reprint, part of start deck or simply new card and then saves the card image into [**images**](./images/) folder. It can be used as standalone app to download card image, however its class' method requires name of a card. It downloades only image for one card at the time, to reduce space occupied by the program.
- **loader.py**: This module is used mostly for initialization part and performing backup operations. It can be used to load data into empty database (not supported in main program functionality) and to perform and load backup.
- **handler.py**: This module is used for utility class *Handler* which allows **main.py** and **gui.py** to access some gui components in an easy way.
- **gui.py**: This modules is used for everything GUI related. It consits of components such as:
    + Image holder, which displays image of current card.
    + Central Frame, which displays information about current card and allows to filter card selection by clan and/or grade.
    + Operation Frame, which allows user to interact through buttons with functionalities of the program, such as adding, editing and deleted a card. Through this window user can also display graphs and perform backup saving operation.

## Example usage
- **Changing the seleted card**:
![Card selection](https://github.com/4DasteR/Cardfight---Vanguard-Card-Manager/assets/66702087/bd06e3f2-4cdf-47f7-8cc2-6f42cebfe60e)
- **Filtering cards by clan and/or grade**:
![Card filtering](https://github.com/4DasteR/Cardfight---Vanguard-Card-Manager/assets/66702087/24feee93-42a1-4b94-89fe-18835214606b)
- **Adding new card**:
![Card add](https://github.com/4DasteR/Cardfight---Vanguard-Card-Manager/assets/66702087/7511c7ee-b93e-435b-a60c-fcf3c2295e59)
- **Editing current card**:
![Card edit](https://github.com/4DasteR/Cardfight---Vanguard-Card-Manager/assets/66702087/8b4fa636-de0e-4d0b-a898-1d5e8f26d012)
- **Deleting current card**:
![Card delete](https://github.com/4DasteR/Cardfight---Vanguard-Card-Manager/assets/66702087/964179c6-89d0-47f0-bb24-4e37a73e51ad)

## Challenges during development
- Getting correct image from website. Originaly displayed image on website is one with smaller resolution, in order to properly download higher resolution image i managed to find it through html **<a>** tag which had the url to higher resoultion image.
- Two before completely unknow tkinter widgets: spinbox and combobox. They were necessary for me to achieve my desired result and I had to learn how to properly configure and use them.
- Creating corelation between GUI CardImageLabel, OperationFrame and CenterFrame which allows them to for example after editing a card in operation frame, update necessary informations in center frame and if necessary update the image in card image label. I overcame it using *handler* approach, which I've seen in past Java game tutorial
- Implementing working editing of a card. The problem with it is that initially card is closely tied to its name, so if I have multiple copies of said card altering one of them without changing the name could have disastrous effects. Ultimately I settled than editing card which has more than one copy can only change its rarity if name is not changed. Otherwise if card got new name (ex. due to naming differences on card itself and wiki entry) all 'new' attributes would be assigned to a new copy of new card.
- On design level solving the issue of having multiple copies of a card. Ultimately I decided to split card logic into two tables in database. *Cards* table holds unique informations about card that are shared among all copies, while *CardInstances* holds information about multiplity and rarity of that card using auto-incremented id for primary_key and cards name for foreign key.
- Problem with displaying label images in CenterFrame. Originally they were part of Application class but in order to separate all GUI components into their own module they were extracted to CenterFrame class. Only problem was that even though Images were created and loaded they did not appear. Ultimately solution was to not only add *image=* argument to constructor of *tk.Label*, but also after that specify image as an attribute *ex_label.**image**=*.

## Learned lessons
- *Seaborn* is actually not an alternative to *matplotlib* but rather its wrapper, which makes using it much simpler and nicer.
- New tkinter widgets, which are actually very useful while creating filters of any kind.
- How to scrap more sophisticated content from websites such as images or movies.
- A lot of things based on [described challenges](#challenges-during-development).

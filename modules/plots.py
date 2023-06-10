"""
    This module is responsible for creation of graphs
"""
import seaborn as sns
from modules.DAO import DAO
import pandas as pd
import matplotlib.pyplot as plt

def card_grade_distribution(dao: DAO):
    """
    Creates graph of card distribution among grades

    Args:
        dao (DAO): Database Access Object.
    """
    plt.close()
    results = dao.get_cards_grades_count()
    grades = []
    counts = []
    for group in results:
        grades.append(group[0])
        counts.append(group[1])
        
    data = {'Grade':grades, 'Count':counts}
    df = pd.DataFrame(data)
    ax = sns.barplot(data=df, x='Grade', y='Count')
    
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    plt.xlabel('Grade')
    plt.ylabel('Count')
    plt.title('Distribution of cards on Grade')
    plt.show()

def card_clan_distribution(dao: DAO):
    """
    Creates graph of card distribution among clans

    Args:
        dao (DAO): Database Access Object.
    """
    plt.close()
    results = dao.get_cards_clan_count()
    clans = []
    counts = []
    for group in results:
        clans.append(group[0])
        counts.append(group[1])
        
    data = {'Clans':clans, 'Count':counts}
    df = pd.DataFrame(data)
    ax = sns.barplot(data=df, y='Clans', x='Count')
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))

    plt.ylabel('Clan')
    plt.xlabel('Count')
    plt.title('Distribution of cards on Clans')
    plt.show()
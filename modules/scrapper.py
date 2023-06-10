"""
    This module provides implementation of web scrapping to receive image of card from official wiki of 'Cardfight!! Vanguard'.
"""
import requests
from bs4 import BeautifulSoup
import re

class Scrapper():
    """
    Class represending a Scrapper utility mechanism.
    
    Attributes:
        card_url (str): url to the wiki website.
        
    Methods:
        extract_image -- performs web scrapping for image of the card on the website.
        First it searches in the link with suffix "_(V_Series)", since card can be a reprint from original series.
        If image is not found it repeats above process for link with suffix "_(V_Series_Start_Deck)".
        Otherwise it searches for image inside of pure link without any suffixes.
        Returns True if image was found, otherwise False.
    """
    card_url = 'https://cardfight.fandom.com/wiki/'

    def extract_image(self, name: str):
        url = self.card_url + name.replace(' ', '_') + "_(V_Series)"
        pattern = re.compile(r'(V|D)-[a-zA-Z0-9]{2,4}-[a-zA-Z0-9]{4,5}(-\w+|\s+\(Sample\))*')

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')  # Get all images on the website

        if not any(pattern.findall(str(img)) for img in images):
            # Retry with "_(V_Series_Start_Deck)" if desired card image is not a reprint
            url = self.card_url + name.replace(' ', '_') + "_(V_Series_Start_Deck)"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            images = soup.find_all('img')

            if not any(pattern.findall(str(img)) for img in images):
                # Retry without any suffix if desired card image is not a reprint
                url = self.card_url + name.replace(' ', '_')
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                images = soup.find_all('img')

        if len(images) >= 2:
            # Look for the image of the card with a link to the higher resolution image
            if any(pattern.findall(str(img)) for img in images):
                image_highres_link = images[1].find_previous('a')

                if image_highres_link and image_highres_link.has_attr('href'):
                    image_highres_url = image_highres_link['href']
                    image_highres = requests.get(image_highres_url)

                    file_path = f'images/{name}.jpg'
                    with open(file_path, 'wb') as image_file:
                        image_file.write(image_highres.content)

                    return True

        return False
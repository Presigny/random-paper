"""Open a random scientific paper on web browser with a given archive (arXiv, PubMed...).
Usage:
======
    user have to change parameters in the main

    provider: a string which specifies the archive to search in
    webpages: an integer which specifies the number of random webpages to open for the run
"""
__authors__ = ("Charley Presigny")
__contact__ = ("charley.presigny@inria.fr")
__version__ = "1.0.0"
__copyright__ = "CC BY 4.0"
__date__ = "2020/11"

import csv
from random import seed,randrange
from time import time
import webbrowser

class Code:
    """Load the desired archive data (if any)

    After being initialized for a given archive, instances of this class
    provide a method to generate a random code (corresponding to a paper)
    and to open the related webpages in the web browser
    """

    def __init__(self, provider='arXiv'):
        """Select the instance to create accordinf to the user's choice"""
        self.list_of_provider = ['arXiv','PubMed']
        self.provider = provider
        if self.provider == 'arXiv':
            self.generator = ArXivGen()
        elif self.provider == 'PubMed':
            self.generator = PubMedGen()
        else:
            raise Exception("Archive provider not available. Available providers: arXiv, PubMed")

    def get_id(self):
        """Generate the random code associated with a paper and a given archive"""
        self.code = self.generator.code()
        return self.code

    def get_url(self):
        """Generate the url associated with the current random code in 'generator'"""
        return self.generator.get_url()

class ArXivGen:
    """Select a random paper on arXiv from April 2007 to October 2020"""
    def __init__(self):
        """Load the required data to generate an ArXiv number"""
        self.load_arxiv_data()
        self.prefix_generator()

    def load_arxiv_data(self):
        """load the data file of the number of paper published each month on arXiv"""
        self.l_articles = []
        with open('arvix_database.txt','r') as data:
            read_data = csv.reader(data, delimiter=',', quotechar='|')
            for row in read_data:
                self.l_articles.append(int(row[1]))
        return 0

    def prefix_generator(self):
        """Generate the firt part of an ArXiv code (year and month of the publication)"""
        self.l_prefix = ['0704'] # minimal code prefix corresponding to paper published on April 2007
        year = 7
        month = 4
        for i in range(len(self.l_articles)):
            month += 1
            if month > 12:
                month = 1
                year += 1
            if len(str(year*100+month)) == 4:
                prefix = str(year * 100 + month)
                self.l_prefix.append(prefix)
            else:
                prefix = '0'+str(year * 100 + month)
                self.l_prefix.append(prefix)
        return 0

    def code(self):
        """Generate the random code and stock the url in the instance"""
        seed(time())
        draw = randrange(0,len(self.l_articles),1)
        prefix = self.l_prefix[draw]
        suffix = str(randrange(0,self.l_articles[draw],1))
        diff = 5-len(suffix)
        for i in range(diff):
            suffix = '0'+suffix
        code = prefix+'.'+suffix
        self.url = 'https://arxiv.org/abs/'+ code
        return code

    def get_url(self):
        return self.url

class PubMedGen:
    """Select a random paper on PubMed published up to 10/31/2020"""
    def __init__(self):
        self.max = 33129233 # PMID number of the last paper published on 10/31/2020
        self.min = 10000000 # empirical minimal PMID number

    def code(self):
        """Generate the random code and stock the url in the instance"""
        seed(time())
        draw = str(randrange(self.min,self.max,1))
        self.url = 'https://pubmed.ncbi.nlm.nih.gov/'+ draw
        return draw

    def get_url(self):
        return self.url

if __name__ == "__main__":

    """Here begins the principal program."""

    provider = 'arXiv'
    webpages = 1

    for i in range(webpages):
        drawing = Code(provider)
        number = drawing.get_id()
        print("The " + provider + " generated number is: " + number)
        webbrowser.open(drawing.get_url())

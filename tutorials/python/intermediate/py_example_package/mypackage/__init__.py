import random
import pkgutil

class MyPackage:
    
    def __init__(self):
        pass
    
    def random_word(self):
        try:
            with open('data/words.txt') as f:
                words = f.read().splitlines()
        except:
            words = pkgutil.get_data(__name__, "data/words.txt").decode('utf-8').splitlines()
        return random.choice(words)
    
    def sum(self, x, y):
        return x + y
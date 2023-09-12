import os

class Path():
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
    
    def get_path(self):
        return self.dir_path
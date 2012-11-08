import tarfile

class TetrisData:
    
    def __init__(self):
        try:
            self.data = tarfile.open("data.cbx", 'r:gz')
        except:
            print 'ERROR: data.cbx not found'
    
    
    def get(self, file):
        try:
            return self.data.extractfile(file)
        except:
            return None
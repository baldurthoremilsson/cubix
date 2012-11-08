from Image import *
from xml.dom import minidom, Node

class TextureString:
    
    def __init__(self, data):
        self.data = {}
        self.height = 0
        
        # texture information
        doc = minidom.parse(data.get("texture/font/paths.xml"))
        for letter in doc.getElementsByTagName('letter'):
            name = letter.getElementsByTagName('name')[0].childNodes[0].nodeValue
            path = 'texture/font/' + letter.getElementsByTagName('path')[0].childNodes[0].nodeValue
            offset = letter.getElementsByTagName('offset')[0].childNodes[0].nodeValue
            image = open(data.get(path))
            self.data[name] = {'image': image, 'offset': offset, 'width': image.size[0], 'height': image.size[1]}
            if self.height < image.size[1]: self.height = image.size[1]
        #texture information
        self.height = int(self.height * 1.1)
        self.line = int(self.height * 0.75)
    
    def create(self, string, name = None):
        image = new("RGBA",(0,self.height))
        for letter in string:
            try:
                subimg = self.data[letter]['image']
            except:
                subimg = new('RGBA',(0,0))
            offset = int(self.data[letter]['offset'])
            
            temp = image.copy()
            
            upper = self.line - offset
            lower = upper + subimg.size[1]
            
            image = new('RGBA', (temp.size[0] + subimg.size[0], image.size[1]))
            image.paste(temp,(0, 0, temp.size[0], temp.size[1]))
            image.paste(subimg, (temp.size[0], upper, image.size[0], lower))
        return image
    '''
    box = (100, 100, 400, 400) -> (left, upper, right, lower)
    o---
    |  |
    ---o
    '''
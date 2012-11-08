from Image import *
from GameObject import *

class Textures:
    
    def createTex(self, file, id = None):
        try:
            image = open(file)
        except:
            image = file
        
        ix = image.size[0]
        iy = image.size[1]
        
        if image.format == 'PNG':
            image = image.tostring("raw", "RGBA", 0, -1)
        elif image.format == 'JPEG':
            image = image.tostring("raw", "RGBX", 0, -1)
        else:
            image = image.tostring("raw", "RGBA", 0, -1)
        
        if id == None:
            self.id = glGenTextures(1)
        else:
            self.id = id
        
        glBindTexture(GL_TEXTURE_2D, self.id)
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,2)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA16, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        return self.id
        
    def deleteTex(self,id):
        glDeleteTextures(id)
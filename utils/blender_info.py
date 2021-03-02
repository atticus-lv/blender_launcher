import os
import time

class Blender():
    """
    :parm bl_info:{
                    'name'      : self.name,
                    'build_time': self.build_time,
                    'path'      : self.path,
                    'version'   : self.version,
                    }
    """

    def __init__(self, path):
        self.bl_info = {}
        self.generate_info_dict(path)

    def generate_info_dict(self, path):
        dir = path.replace('\n', '')

        try:
            self.path = os.path.join(dir, 'blender.exe')
            dirname = os.path.basename(os.path.dirname(self.path))

            try:
                version = dirname.split('-')[1]
            except:
                version = dirname[7:]

            self.name = dirname
            self.version = version
            self.build_time = time.ctime(os.stat(self.path).st_mtime)
            # dict
            self.bl_info = {
                'name'      : self.name,
                'build_time': self.build_time,
                'path'      : self.path,
                'version'   : self.version,
            }
        except Exception:
            self.path = None
            self.bl_info = {}

import os,sys
import shutil
from necroposter import necroposter

class storage():
    def __init__(self,path, np_obj):
        '''init data structures'''
        self.path=os.path.join(path,".anime")
        self.np=np_obj

        self.data=os.path.join(self.path, "data.cache")
        self.cover=os.path.join(self.path, "cover.jpg")
        self.studio=os.path.join(self.path, "studio.jpg")
        self.mini=os.path.join(self.path, "mini.jpg")
        self.store_pic_multi()
        self.store_data()

    def init(self):
        self.mkdir(self.path)

    def mkdir(self, dir):
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def store_pic_multi(self):
        self.store_pic(self.np.imglink['fname'],self.cover)
        self.store_pic(self.np.studio['fname'],self.studio)

    def store_pic(self, pic_url, dst):
        shutil.copy(pic_url,dst)


def main(n):
        if len(n) == 0:
                print "Give pagenumber or full link as an argument"
                sys.exit(1)
        else:
                np=necroposter()
                np.dw_wapage('6714')
                np.init_data()
                s=storage(n[0],np)
                s.init()

if __name__ == "__main__":
    main(sys.argv[1:])


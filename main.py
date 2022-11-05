from PyQt5.QtWidgets import *
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import os

app = QApplication([])
window = QWidget()
window.resize(700,400)

dir_btn=QPushButton('Папка')
left_btn=QPushButton('Лево')
right_btn=QPushButton('Право')
mir_btn=QPushButton('Зеркало')
sharp_btn=QPushButton('Резкость')
bw_btn=QPushButton('Ч/Б')

dir_list=QListWidget()
paint=QLabel('Картинка')

vline1=QVBoxLayout()
vline2=QVBoxLayout()
hline1=QHBoxLayout()
main_line=QHBoxLayout()

vline1.addWidget(dir_btn)
vline1.addWidget(dir_list)

hline1.addWidget(left_btn)
hline1.addWidget(right_btn)
hline1.addWidget(mir_btn)
hline1.addWidget(sharp_btn)
hline1.addWidget(bw_btn)

vline2.addWidget(paint)
vline2.addLayout(hline1)
main_line.addLayout(vline1, 20)
main_line.addLayout(vline2,80)
window.setLayout(main_line)

window.show()

workdir=''
def choseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result=list()
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilternamesList():
    choseWorkDir()
    extensions=['.jpg','.jpeg','.png','.gif','.bmp']
    files=filter(os.listdir(workdir),extensions)
    dir_list.clear()
    for filename in files:
        dir_list.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.image=None
        self.filename=None
        self.und_dir='modified/'
        self.name_dir=None

    def loadImage(self, filename, name_dir):
        self.filename = filename
        self.name_dir = name_dir
        file_path = os.path.join(name_dir, filename)
        self.image = Image.open(file_path)

    def showImage(self, path):
        paint.hide()
        pixmapimage = QPixmap(path)
        w, h=paint.width(), paint.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        paint.setPixmap(pixmapimage)
        paint.show()

    def do_bw(self):
        self.image=self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.name_dir, self.und_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.name_dir, self.und_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.name_dir, self.und_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.name_dir, self.und_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.name_dir, self.und_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.name_dir, self.und_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path=os.path.join(path, self.filename)
        self.image.save(image_path)

def showChosenImage():
    if dir_list.currentRow() >= 0:
        filename = dir_list.currentItem().text()
        workimage.loadImage(filename, workdir)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

workimage=ImageProcessor()

mir_btn.clicked.connect(workimage.do_flip)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
sharp_btn.clicked.connect(workimage.do_sharp)
bw_btn.clicked.connect(workimage.do_bw)
dir_btn.clicked.connect(showFilternamesList)
dir_list.currentRowChanged.connect(showChosenImage)


app.exec()
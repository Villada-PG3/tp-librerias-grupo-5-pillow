from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QAction, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label, 1)

        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)

        self.load_button = QPushButton('Open Image', self)
        self.load_button.clicked.connect(self.open_image)
        controls_layout.addWidget(self.load_button)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.save_image)
        controls_layout.addWidget(self.save_button)

        brightness_layout = QVBoxLayout()
        controls_layout.addLayout(brightness_layout)
        brightness_layout.addWidget(QLabel("Brightness"))

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.adjust_brightness)
        brightness_layout.addWidget(self.brightness_slider)

        contrast_layout = QVBoxLayout()
        controls_layout.addLayout(contrast_layout)
        contrast_layout.addWidget(QLabel("Contrast"))

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(-100)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)
        contrast_layout.addWidget(self.contrast_slider)

        saturation_layout = QVBoxLayout()
        controls_layout.addLayout(saturation_layout)
        saturation_layout.addWidget(QLabel("Saturation"))

        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setMinimum(-100)
        self.saturation_slider.setMaximum(100)
        self.saturation_slider.setValue(0)
        self.saturation_slider.valueChanged.connect(self.adjust_saturation)
        saturation_layout.addWidget(self.saturation_slider)

        rotation_flip_layout = QHBoxLayout()
        controls_layout.addLayout(rotation_flip_layout)

        self.rotate_left_button = QPushButton('Rotate Left', self)
        self.rotate_left_button.clicked.connect(self.rotate_left)
        rotation_flip_layout.addWidget(self.rotate_left_button)

        self.rotate_right_button = QPushButton('Rotate Right', self)
        self.rotate_right_button.clicked.connect(self.rotate_right)
        rotation_flip_layout.addWidget(self.rotate_right_button)

        self.flip_horizontal_button = QPushButton('Flip Horizontal', self)
        self.flip_horizontal_button.clicked.connect(self.flip_horizontal)
        rotation_flip_layout.addWidget(self.flip_horizontal_button)

        self.flip_vertical_button = QPushButton('Flip Vertical', self)
        self.flip_vertical_button.clicked.connect(self.flip_vertical)
        rotation_flip_layout.addWidget(self.flip_vertical_button)

        self.image = None
        self.original_image = None

    def open_image(self):
        file_dialog = QFileDialog(self)
        filepath, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if filepath:
            self.image = Image.open(filepath)
            self.original_image = self.image.copy()  # Hacer una copia de la imagen original
            self.display_image()

    def save_image(self):
        if self.image:
            file_dialog = QFileDialog(self)
            filepath, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
            if filepath:
                self.image.save(filepath)

    def display_image(self):
        if self.image:
            img = self.image.convert("RGBA")
            img.thumbnail((780, 480))
            image_data = img.tobytes('raw', 'RGBA')
            qimage = QImage(image_data, img.size[0], img.size[1], QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)

    def adjust_brightness(self, value):
        if self.image is not None:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.image = enhancer.enhance((value + 100) / 100)
            self.display_image()
        else:
            print("Error: No se ha cargado ninguna imagen.")

    def adjust_contrast(self, value):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.image = enhancer.enhance((value + 100) / 100)
            self.display_image()
    
    def adjust_saturation(self, value):
        if self.image:
            enhancer = ImageEnhance.Color(self.original_image)
            self.image = enhancer.enhance((value + 100) / 100)
            self.display_image()

    def rotate_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.display_image()

    def rotate_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.display_image()

    def flip_horizontal(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image()

    def flip_vertical(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.display_image()

if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.png'))  # Cambiar 'icon.png' por el nombre de tu archivo de icono
    editor = ImageEditor()
    editor.show()
    app.exec_()

general_style = """
QWidget {
     background-color: #2b2b2b;
 }

 QLabel {
     color: #ffffff;
     font-size: 16px;
 }

 QSlider {
     min-height: 25px;
     max-height: 25px;
 }

 QSlider::groove:horizontal {
     height: 10px;
     background: #525252;
     margin: 0px;
     border-radius: 5px;
 }

 QSlider::handle:horizontal {
     background-color: #ff5a1f;
     border: none;
     height: 20px;
     width: 20px;
     margin: -5px 0;
     border-radius: 10px;
 }

 QSlider::groove:horizontal:hover {
     background: #424242;
 }

 QSlider::handle:horizontal:hover {
     background-color: #e65f23;
 }

 QSlider::groove:horizontal:pressed {
     background: #333333;
 }

 QSlider::handle:horizontal:pressed {
     background-color: #ff3218;
 }

 QPushButton {
     background-color: #ff5a1f;
     border: none;
     color: white;
     padding: 15px;
     text-align: center;
     text-decoration: none;
     font-size: 16px;
     margin: 4px 2px;
     border-radius: 10px;
 }
"""

anime_button = """
QPushButton {
    background-color: #ff5a1f;
    color: #FFFFFF;
    border: none;
}
QPushButton:hover {
    background-color: #eb3e00;
}
QPushButton:pressed {
    background-color: #8B4513;
}
"""

pdf_button = """
QPushButton {
    background-color: #008080;
    color: #FFFFFF;
    border: none;
}
QPushButton:hover {
    background-color: #006767;
}
QPushButton:pressed {
    background-color: #004646;
}
"""

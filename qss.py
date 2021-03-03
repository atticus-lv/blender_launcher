dark = """
/* WHITE THEME FOR BLENDER LAUNCHER*/


QCheckBox {
  spacing: 5px;
}

QCheckBox::indicator {
  width: 32px;
  height: 32px;
}

QCheckBox::indicator:unchecked {
  image: url(":/img/slider2.png");
}

QCheckBox::indicator:checked {
  image: url(":/img/slider_check2.png");
}


QFrame {
  border-radius：10px;
}

QFrame#drop_shadow_frame {
  border-radius：10px;
  border-image: url(":/img/bg2.png");
}


QComboBox {
  background-color: #55B0FF;
  color: white;
  padding: 20px;

  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
}


QComboBox:hover {
  background-color: white;
  color: black;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 30px;

  border-top-right-radius: 3px; /* same radius as the QComboBox */
  border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
  border-image: url(":/img/arrow_down.png");
}


QPushButton#launch_button {
  background-color: #55B0FF;
  color: white;

  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

QPushButton#launch_button:hover {
  background-color: white;
  color: black;
}

QPushButton#btn_close {
  border: none;
  border-radius: 4px;
  background-color: white;
}

QPushButton#btn_close:hover {
  background-color: rgb(255, 255, 255, 150);
}


QPushButton#btn_minimize {
  border: none;
  border-radius: 4px;
  background-color: white;
}

QPushButton#btn_minimize:hover {
  background-color: rgb(255, 255, 255, 150);
}


QPushButton#btn_preference {
  border: none;
  border-radius: 15px;
  background-color: none;
}

QPushButton#btn_preference:hover {
  background-color: #55B0FF;
}

QPushButton#btn_home {
  border: none;
  border-radius: 15px;
  background-color: none;
}

QPushButton#btn_home:hover {
  background-color: #55B0FF;
}

QPushButton#btn_list_remove {
  border: none;
  background-color: #55B0FF;
}

QPushButton#btn_list_remove:hover {
  background-color: rgb(255, 220, 0);
}



QListView#blender_folder_list {
  background: black;
  color:white;
  border: 2 solid grey;
  border-radius: 5px;
}

/* setAlternatingRowColors(true); */

QListView#blender_folder_list::item:alternate {
  color: white;
  background: rgb(55,55,55);
}

QListView#blender_folder_list::item:selected {
  color: white;
  background-color: dodgerblue;
}

QListView#blender_folder_list::item::hover {
  background: #55B0FF;
  padding: 10px;
}


QLabel#label_credits {
  color: rgb(170, 170, 170);
}

QLabel#label_title {
  color: white;
  padding-left: 15px;
}


QLabel#blender_info {
  color: white;
  padding-left: 15px;
}
"""

white = """
/* WHITE THEME FOR BLENDER LAUNCHER*/


QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 32px;
    height: 32px;
}

QCheckBox::indicator:unchecked {
    image: url(":/img/slider.png");
}
QCheckBox::indicator:checked {
    image: url(":/img/slider_check.png");
}




QFrame {
  border-radius：10px;
}

QFrame#drop_shadow_frame {
  border-radius：10px;
  border-image: url(":/img/bg.png");
}

QComboBox {
  background-color: rgb(255, 170, 0);
  color: white;
  padding: 20px;

  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
}

QComboBox:hover {
  background-color: rgb(255, 220, 0);
  color: white;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 30px;

  border-top-right-radius: 3px; /* same radius as the QComboBox */
  border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
  border-image: url(:/img/arrow_down.png);
}

QPushButton#launch_button {
  background-color: rgb(255, 170, 0);
  color: white;

  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

QPushButton#launch_button:hover {
  background-color: rgb(255, 220, 0);
  color: white;
}

QPushButton#btn_close {
  border: none;
  border-radius: 4px;
  background-color: rgb(255, 0, 0, 255);
}

QPushButton#btn_close:hover {
  background-color: rgb(255, 0, 0, 150);
}


QPushButton#btn_minimize {
  border: none;
  border-radius: 4px;
  background-color: rgb(85, 255, 127, 255);
}

QPushButton#btn_minimize:hover {
  background-color: rgb(85, 255, 127, 150);
}


QPushButton#btn_preference {
  border: 2px solid orange;
  border-radius: 15px;
  background-color: none;
}

QPushButton#btn_preference:hover {
  background-color: orange;
}

QPushButton#btn_home {
  border: 2px solid orange;
  border-radius: 15px;
  background-color: none;
}

QPushButton#btn_home:hover {
  background-color: orange;
}

QPushButton#btn_list_remove {
  border: none;
  background-color: orange;
}

QPushButton#btn_list_remove:hover {
  background-color: rgb(255, 220, 0);
}

QPushButton#btn_list_refresh {
  border: none;
  background-color: orange;
  border-radius: 15px;
}

QPushButton#btn_list_refresh:hover {
  background-color: rgb(255, 220, 0);
}

/*
list
*/

QListView#blender_folder_list{
  border: 2 solid orange;
  border-radius: 5px;
  alternate-background-color: orange;
  
}


QListView#blender_folder_list::item:alternate {
  background: #D9FAFF;
}

QListView#blender_folder_list::item:selected {
  color: white;
  background-color: orange;
}

QListView#blender_folder_list::item::hover {
  background: rgb(0, 170, 255);
  padding: 10px;
}


QLabel#label_credits {
  color: rgb(170, 170, 170);
}

QLabel#label_title {
  color: rgb(57, 57, 57);
  padding-left: 15px;
}


QLabel#blender_info {
  color: rgb(57, 57, 57);
  padding-left: 15px;
}

QScrollBar{
background:orange;
}

QScrollBar::handle
{
    width:10px;
    background:orange;
    border-radius:10px;   
    min-height:20;
}

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, \
    QGroupBox, QProgressBar, QSpacerItem, QSizePolicy, QListWidget, QListWidgetItem, QMenuBar, QMenu, QAction, \
    QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, Qt, QModelIndex, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
import json
import os
import sys


class musicplayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 窗体

        self.icon_size = 25
        self.setFixedSize(450, 500)
        self.setWindowTitle('Music Player')
        self.setWindowIcon(QIcon('musicplayer.png'))

        # 菜单
        menubar = self.menuBar()
        menu = QMenu("文件", self)
        menubar.addMenu(menu)

        # QAction绑定事件
        open_folder_action = QAction('选择文件夹', self)
        open_folder_action.triggered.connect(self.select_folder)
        menu.addAction(open_folder_action)

        # 上布局
        uplayout = QHBoxLayout()
        self.setLayout(uplayout)

        self.pixlabel = QLabel(self)
        self.pixlabel.setFixedSize(320, 320)
        self.pixlabel.setAlignment(Qt.AlignCenter)
        self.songlist = QListWidget(self)
        self.songlist.setMaximumHeight(320)
        uplayout.addWidget(self.songlist)
        uplayout.addWidget(self.pixlabel)
        self.songlist.hide()

        # 中间布局
        middlelayout = QHBoxLayout()
        middlelayout.addStretch(1)  # 添加一个弹簧
        self.setLayout(middlelayout)
        self.timebar = QProgressBar(self)
        self.timebar.setFixedWidth(460)
        self.timebar.setOrientation(Qt.Orientation.Horizontal)
        self.timebar.valueChanged.connect(self.on_progress_changed)
        middlelayout.addWidget(self.timebar)
        middlelayout.addStretch(1)  # 添加另一个弹簧

        # 下布局，使用 QHBoxLayout 水平布局管理左中右三个结构体
        downlayout = QHBoxLayout()
        downlayout.addStretch(0.5)

        # 按钮
        self.play_button = QPushButton()
        self.play_button.resize(self.icon_size, self.icon_size)
        self.play_button.setIcon(QIcon('播放.png'))
        self.play_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.play_button.clicked.connect(self.on_play_button_clicked)

        self.pause_button = QPushButton()
        self.pause_button.resize(self.icon_size, self.icon_size)
        self.pause_button.setIcon(QIcon('暂停.png'))
        self.pause_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.pause_button.clicked.connect(self.on_pause_button_clicked)

        self.pre_button = QPushButton()
        self.pre_button.resize(self.icon_size, self.icon_size)
        self.pre_button.setIcon(QIcon('上一首.png'))
        self.pre_button.setIconSize(QSize(self.icon_size, self.icon_size))

        self.next_button = QPushButton()
        self.next_button.resize(self.icon_size, self.icon_size)
        self.next_button.setIcon(QIcon('下一首.png'))
        self.next_button.setIconSize(QSize(self.icon_size, self.icon_size))

        self.volume_button = QPushButton()
        self.volume_button.resize(30, 30)
        self.volume_button.setIcon(QIcon('音量.png'))
        self.volume_button.setIconSize(QSize(self.icon_size, self.icon_size))

        self.volume_bar = QSlider()
        # self.volume_bar.setOrientation(1)  # 设置为垂直方向
        self.volume_bar.setOrientation(Qt.Orientation.Vertical)
        self.volume_bar.valueChanged.connect(self.on_volume_changed)
        self.volume_bar.setGeometry(10, 10, 20, 200)
        self.volume_bar.setRange(0, 100)  # 设置最大最小值
        self.volume_bar.setSliderPosition(50)  # 设置初始值 50
        self.volume_bar.setTickPosition(QSlider.TicksBothSides)  # 设置刻度位置在两侧

        self.shuffle_button = QPushButton()
        self.shuffle_button.resize(self.icon_size, self.icon_size)
        self.shuffle_button.setIcon(QIcon('随机.png'))
        self.shuffle_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.shuffle_button.clicked.connect(self.on_shuffle_button_clicked)
        self.shuffle_button.setCheckable(True)

        self.repeat_button = QPushButton()
        self.repeat_button.resize(self.icon_size, self.icon_size)
        self.repeat_button.setIcon(QIcon('重复.png'))
        self.repeat_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.repeat_button.clicked.connect(self.on_repeat_button_clicked)
        self.repeat_button.setCheckable(True)

        self.songlist_play_button = QPushButton()
        self.songlist_play_button.resize(self.icon_size, self.icon_size)
        self.songlist_play_button.setIcon(QIcon('列表循环.png'))
        self.songlist_play_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.songlist_play_button.clicked.connect(self.on_songlist_play_button_clicked)
        self.songlist_play_button.setCheckable(True)

        self.songlist_button = QPushButton()
        self.songlist_button.resize(self.icon_size, self.icon_size)
        self.songlist_button.setIcon(QIcon('歌单.png'))
        self.songlist_button.setIconSize(QSize(self.icon_size, self.icon_size))
        self.songlist_button.setCheckable(True)
        self.songlist_button.clicked.connect(self.songlist_toggle)

        self.repeat_button.hide()
        self.songlist_play_button.hide()
        self.pause_button.hide()

        # 按钮分为左中右区域
        left_group_box = QGroupBox()
        left_group_box.setFixedWidth(100)
        left_group_box.setFixedHeight(70)
        left_button_area = QHBoxLayout()

        right_group_box = QGroupBox()
        right_button_area = QHBoxLayout()
        right_group_box.setFixedHeight(70)
        right_group_box.setFixedWidth(100)

        middle_group_box = QGroupBox()
        middle_button_area = QHBoxLayout()
        middle_group_box.setFixedHeight(70)
        middle_group_box.setFixedWidth(200)

        # 左侧添加按钮
        left_button_area.addWidget(self.songlist_button)
        left_button_area.addWidget(self.shuffle_button)
        left_button_area.addWidget(self.repeat_button)
        left_button_area.addWidget(self.songlist_play_button)
        left_group_box.setLayout(left_button_area)

        # 中间添加按钮
        middle_button_area.addWidget(self.pre_button)
        middle_button_area.addWidget(self.play_button)
        middle_button_area.addWidget(self.pause_button)
        middle_button_area.addWidget(self.next_button)
        middle_group_box.setLayout(middle_button_area)

        # 右侧添加按钮
        right_button_area.addWidget(self.volume_button)
        right_button_area.addWidget(self.volume_bar)
        right_group_box.setLayout(right_button_area)

        # 添加到下布局
        downlayout.addWidget(left_group_box)
        downlayout.addWidget(middle_group_box)
        downlayout.addWidget(right_group_box)
        downlayout.addStretch(0.5)

        # 使用 QVBoxLayout 垂直布局管理上中下三个部分
        all_layout = QVBoxLayout()
        all_layout.addLayout(uplayout)
        all_layout.addLayout(middlelayout)
        all_layout.addLayout(downlayout)

        self.player = QMediaPlayer(self)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.positionChanged.connect(self.position_changed)
        
        widget = QWidget()
        widget.setLayout(all_layout)
        self.setCentralWidget(widget)

    def on_progress_changed(self):
        self.player.setPosition(self.timebar.value())

    def position_changed(self, position):
        self.timebar.setValue(position)

    def on_volume_changed(self, value):
        print("当前音量：", value)

    def on_play_button_clicked(self):
        if not self.player.currentMedia().canonicalUrl().isEmpty():
            self.play_button.hide()
            self.pause_button.show()
            self.player.play()
            self.play_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def on_pause_button_clicked(self):
        self.player.pause()
        self.pause_button.hide()
        self.play_button.show()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def on_shuffle_button_clicked(self):
        self.shuffle_button.hide()
        self.songlist_play_button.hide()
        self.repeat_button.show()

    def on_repeat_button_clicked(self):
        self.repeat_button.hide()
        self.shuffle_button.hide()
        self.songlist_play_button.show()

    def on_songlist_play_button_clicked(self):
        self.songlist_play_button.hide()
        self.repeat_button.hide()
        self.shuffle_button.show()

    def songlist_toggle(self):
        if self.songlist.isVisible():
            self.songlist.hide()
        else:
            self.songlist.show()

    def select_folder(self):
        self.songlist.clear()  # 添加前清空
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            file_names = os.listdir(folder_path)
            for file_name in file_names:
                if '.mp3' in file_name or '.wma' in file_name:
                    self.songlist.addItem(QListWidgetItem(file_name))
                    media_content = QMediaContent(QUrl.fromLocalFile(os.path.join(folder_path, file_name)))
                    self.player.setMedia(media_content)
                    self.player.metaDataChanged.connect(lambda: self.update_pixmap(self.player))
        if not folder_path:
            return 
            
        self.setWindowTitle(f"Music Player - {folder_path}")
        
    def media_status_changed(self):
        ms = self.player.mediaStatus()
        if ms == QMediaPlayer.EndOfMedia:
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            if self.repeat_button.isChecked():
                self.player.play()
                
            elif self.shuffle_button.isChecked():
                if self.songlist.count() > 1:
                    song = self.songlist.item(0)
                    current_song = self.player.currentMedia().canonicalUrl().fileName()
                    while song.text() == current_song:
                        self.songlist.takeItem(0)
                        self.songlist.addItem(song)
                        song = self.songlist.item(0)
                        current_song = self.player.currentMedia().canonicalUrl().fileName()
                    index = self.songlist.indexFromItem(song).row()
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(song.data(Qt.UserRole))))
                    self.player.playlist().setCurrentIndex(index)
                    self.player.play()

            elif self.songlist_play_button.isChecked():
                if self.songlist.count() > 1:
                    song = self.songlist.item(0)
                    while song == self.player.currentMedia().canonicalUrl().fileName():
                        self.songlist.takeItem(0)
                        self.songlist.addItem(song)
                        song = self.songlist.item(0)
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(song.data(Qt.UserRole))))
                    self.player.play()
                    
        elif ms == QMediaPlayer.LoadedMedia:
            self.timebar.setRange(0, self.player.duration())
            self.timebar.setValue(0)

    def update_pixmap(self, media_player):
        pixmap = QPixmap()
        if media_player.isMetaDataAvailable():
            metadata = media_player.metaData(QMediaMetaData.AllMetaData)
            cover = metadata.get(QMediaMetaData.CoverArtImage)
            if cover:
                pixmap.loadFromData(cover)
        self.pixlabel.setPixmap(pixmap)
        
                                 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mp = musicplayer()
    mp.show()
    sys.exit(app.exec_())

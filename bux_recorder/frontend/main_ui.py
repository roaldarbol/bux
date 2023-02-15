# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_Bux(object):
    def setupUi(self, Bux):
        if not Bux.objectName():
            Bux.setObjectName("Bux")
        Bux.resize(620, 392)
        self.actionUndo = QAction(Bux)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QAction(Bux)
        self.actionRedo.setObjectName("actionRedo")
        self.centralwidget = QWidget(Bux)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSetup = QWidget()
        self.tabSetup.setObjectName("tabSetup")
        self.verticalLayout_3 = QVBoxLayout(self.tabSetup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton = QPushButton(self.tabSetup)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.tabWidget.addTab(self.tabSetup, "")
        self.tabCameras = QWidget()
        self.tabCameras.setObjectName("tabCameras")
        self.verticalLayout_2 = QVBoxLayout(self.tabCameras)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.tabCameras)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 70))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName("pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 0, 3, 1, 1)

        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)

        self.pushButton_7 = QPushButton(self.groupBox_2)
        self.pushButton_7.setObjectName("pushButton_7")

        self.gridLayout.addWidget(self.pushButton_7, 0, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.tabCameras)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName("label")

        self.horizontalLayout_3.addWidget(self.label)

        self.pushButton_8 = QPushButton(self.groupBox)
        self.pushButton_8.setObjectName("pushButton_8")

        self.horizontalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_4 = QPushButton(self.groupBox)
        self.pushButton_4.setObjectName("pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_5 = QPushButton(self.groupBox)
        self.pushButton_5.setObjectName("pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.pushButton_6 = QPushButton(self.tabCameras)
        self.pushButton_6.setObjectName("pushButton_6")

        self.verticalLayout_2.addWidget(self.pushButton_6)

        self.tabWidget.addTab(self.tabCameras, "")
        self.tabMicropython = QWidget()
        self.tabMicropython.setObjectName("tabMicropython")
        self.verticalLayout = QVBoxLayout(self.tabMicropython)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_9 = QPushButton(self.tabMicropython)
        self.pushButton_9.setObjectName("pushButton_9")

        self.verticalLayout.addWidget(self.pushButton_9)

        self.tabWidget.addTab(self.tabMicropython, "")
        self.tabExperiment = QWidget()
        self.tabExperiment.setObjectName("tabExperiment")
        self.tabWidget.addTab(self.tabExperiment, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        Bux.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Bux)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 620, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        Bux.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Bux)
        self.statusbar.setObjectName("statusbar")
        Bux.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton, self.tabWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.retranslateUi(Bux)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Bux)

    # setupUi

    def retranslateUi(self, Bux):
        Bux.setWindowTitle(QCoreApplication.translate("Bux", "Bux", None))
        self.actionUndo.setText(QCoreApplication.translate("Bux", "Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("Bux", "Redo", None))
        self.pushButton.setText(
            QCoreApplication.translate("Bux", "Select directory", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabSetup),
            QCoreApplication.translate("Bux", "Setup", None),
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("Bux", "Available Cameras", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("Bux", "Activate Camera", None)
        )
        self.pushButton_7.setText(
            QCoreApplication.translate("Bux", "Load cameras", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("Bux", "Active cameras", None)
        )
        self.label.setText(QCoreApplication.translate("Bux", "Camera ID", None))
        self.pushButton_8.setText(QCoreApplication.translate("Bux", "Preview", None))
        self.pushButton_4.setText(QCoreApplication.translate("Bux", "Configure", None))
        self.pushButton_3.setText(QCoreApplication.translate("Bux", "Load", None))
        self.pushButton_5.setText(QCoreApplication.translate("Bux", "Save", None))
        self.pushButton_6.setText(
            QCoreApplication.translate("Bux", "Preview All", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabCameras),
            QCoreApplication.translate("Bux", "Cameras", None),
        )
        self.pushButton_9.setText(
            QCoreApplication.translate("Bux", "Load Belay File", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabMicropython),
            QCoreApplication.translate("Bux", "Micropython", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabExperiment),
            QCoreApplication.translate("Bux", "Experiment", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("Bux", "File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("Bux", "Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("Bux", "View", None))

    # retranslateUi

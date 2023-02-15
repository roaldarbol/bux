# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
    QMainWindow,
    QMenu,
    QMenuBar,
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
        Bux.resize(450, 394)
        self.centralwidget = QWidget(Bux)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        Bux.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Bux)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 450, 24))
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

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(Bux)

        QMetaObject.connectSlotsByName(Bux)

    # setupUi

    def retranslateUi(self, Bux):
        Bux.setWindowTitle(QCoreApplication.translate("Bux", "Bux", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("Bux", "Tab 1", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("Bux", "Tab 2", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("Bux", "File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("Bux", "Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("Bux", "View", None))

    # retranslateUi

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowQmoexp.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1082, 637)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* Soft Neumorphic Blue */\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0  #F3F9FF,\n"
"                                stop:1  #E3F0FA);\n"
"    border: 1px solid #C9DDED;           /* base border */\n"
"    border-top-color:    #FFFFFF;        /* highlight edge */\n"
"    border-left-color:   #FFFFFF;\n"
"    border-right-color:  #B3CFE6;        /* shadow edge */\n"
"    border-bottom-color: #B3CFE6;\n"
"    border-radius: 12px;\n"
"    color: #21405A;\n"
"    font-size: 14px;\n"
"    font-weight: 600;\n"
"    padding: 10px 18px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0  #FFFFFF,\n"
"                                stop:1  #EAF4FD);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* invert edges for inset feel */\n"
"    border-top-color:    #B3CFE6;\n"
"    border-left-color:   #B3CFE6;\n"
"    border-right-color:  #FFFFFF;\n"
"    border-bot"
                        "tom-color: #FFFFFF;\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0  #DBEAF6,\n"
"                                stop:1  #CFE2F0);\n"
"    padding-top: 11px;\n"
"    padding-bottom: 9px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: #93A9BC;\n"
"    background: #ECF4FA;\n"
"    border: 1px solid #D6E5F1;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    border: 2px solid #9FCCF0;\n"
"    padding: 9px 17px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainWidget = QWidget(self.centralwidget)
        self.mainWidget.setObjectName(u"mainWidget")
        self.mainWidget.setStyleSheet(u"QWidget {\n"
"    background-color: rgb(232, 236, 236);\n"
"}")
        self.mainWidgetLayout = QVBoxLayout(self.mainWidget)
        self.mainWidgetLayout.setObjectName(u"mainWidgetLayout")

        self.verticalLayout.addWidget(self.mainWidget)

        self.footerWidget = QWidget(self.centralwidget)
        self.footerWidget.setObjectName(u"footerWidget")
        self.horizontalLayout = QHBoxLayout(self.footerWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.footerSpacer)

        self.arcDetectionBtn = QPushButton(self.footerWidget)
        self.arcDetectionBtn.setObjectName(u"arcDetectionBtn")

        self.horizontalLayout.addWidget(self.arcDetectionBtn)

        self.shorCircuitDetectionBtn = QPushButton(self.footerWidget)
        self.shorCircuitDetectionBtn.setObjectName(u"shorCircuitDetectionBtn")

        self.horizontalLayout.addWidget(self.shorCircuitDetectionBtn)


        self.verticalLayout.addWidget(self.footerWidget)

        self.verticalLayout.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.arcDetectionBtn.setText(QCoreApplication.translate("MainWindow", u"Arc Detection", None))
        self.shorCircuitDetectionBtn.setText(QCoreApplication.translate("MainWindow", u"Short Circuit Detection", None))
    # retranslateUi


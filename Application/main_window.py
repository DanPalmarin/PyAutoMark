# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(591, 675)
        MainWindow.setFixedSize(591, 675) # makes it so that you can't resize the window
        MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
        
        # Defining each widget and its properties (from QtDesigner)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox2.setGeometry(QtCore.QRect(20, 70, 551, 101))
        self.groupBox2.setObjectName("groupBox2")
        self.button1 = QtWidgets.QPushButton(self.groupBox2)
        #self.button1.setGeometry(QtCore.QRect(10, 20, 91, 31)) #for 'Windowsvista' style
        self.button1.setGeometry(QtCore.QRect(10, 26, 91, 31)) #for 'Fusion' style
        self.button1.setObjectName("button1")
        self.label1 = QtWidgets.QLabel(self.groupBox2)
        self.label1.setGeometry(QtCore.QRect(110, 30, 151, 21))
        self.label1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label1.setObjectName("label1")
        self.button2 = QtWidgets.QPushButton(self.groupBox2)
        #self.button2.setGeometry(QtCore.QRect(10, 60, 91, 31))
        self.button2.setGeometry(QtCore.QRect(10, 62, 91, 31)) #for 'Fusion' style
        self.button2.setObjectName("button2")
        self.label2 = QtWidgets.QLabel(self.groupBox2)
        self.label2.setGeometry(QtCore.QRect(110, 70, 151, 21))
        self.label2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(self.groupBox2)
        self.label3.setGeometry(QtCore.QRect(380, 70, 151, 21))
        self.label3.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label3.setObjectName("label3")
        self.button3 = QtWidgets.QPushButton(self.groupBox2)
        #self.button3.setGeometry(QtCore.QRect(280, 60, 91, 31))
        self.button3.setGeometry(QtCore.QRect(170, 62, 91, 31)) #for 'Fusion' style
        self.button3.setObjectName("button3")
        self.groupBox1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox1.setGeometry(QtCore.QRect(20, 10, 551, 51))
        self.groupBox1.setObjectName("groupBox1")
        self.radioButton1 = QtWidgets.QRadioButton(self.groupBox1)
        self.radioButton1.setGeometry(QtCore.QRect(10, 15, 131, 41)) #for 'Fusion' style
        #self.radioButton1.setGeometry(QtCore.QRect(20, 10, 131, 41)) #for 'Windowsvista' style
        self.radioButton1.setObjectName("radioButton1")
        self.radioButton2 = QtWidgets.QRadioButton(self.groupBox1)
        #self.radioButton2.setGeometry(QtCore.QRect(170, 10, 131, 41)) #for 'Windowsvista' style
        self.radioButton2.setGeometry(QtCore.QRect(170, 15, 131, 41)) #for 'Fusion' style
        self.radioButton2.setObjectName("radioButton2")
        self.groupBox3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox3.setGeometry(QtCore.QRect(20, 180, 551, 451))
        self.groupBox3.setObjectName("groupBox3")
        self.table1 = QtWidgets.QTableWidget(self.groupBox3)
        self.table1.setGeometry(QtCore.QRect(10, 60, 321, 381))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table1.sizePolicy().hasHeightForWidth())
        self.table1.setSizePolicy(sizePolicy)
        self.table1.setLineWidth(1)
        self.table1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table1.setDragDropOverwriteMode(False)
        self.table1.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table1.setObjectName("table1")
        self.table1.setColumnCount(2)
        self.table1.setRowCount(0)
        
        item = QtWidgets.QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(1, item)
        self.table1.horizontalHeader().setVisible(True)
        self.table1.horizontalHeader().setCascadingSectionResizes(False)
        #self.table1.horizontalHeader().setDefaultSectionSize(100)
        self.table1.setColumnWidth(0,190)
        self.table1.setColumnWidth(1,50)
        self.table1.horizontalHeader().setStretchLastSection(True)
        self.table1.verticalHeader().setVisible(True)
        self.table1.verticalHeader().setCascadingSectionResizes(False)
        self.table1.verticalHeader().setHighlightSections(True)
        self.table1.verticalHeader().setSortIndicatorShown(False)
        self.table1.verticalHeader().setStretchLastSection(False)
        
        self.list1 = QtWidgets.QListWidget(self.groupBox3)
        self.list1.setGeometry(QtCore.QRect(350, 60, 191, 341))
        self.list1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list1.setObjectName("list1")
        self.button6 = QtWidgets.QPushButton(self.groupBox3)
        self.button6.setGeometry(QtCore.QRect(350, 410, 191, 31))
        self.button6.setObjectName("button6")
        self.button4 = QtWidgets.QPushButton(self.groupBox3)
        #self.button4.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.button4.setGeometry(QtCore.QRect(10, 25, 91, 31))
        self.button4.setObjectName("button4")
        # self.button5 = QtWidgets.QPushButton(self.groupBox3)
        # self.button5.setGeometry(QtCore.QRect(110, 20, 91, 31))
        # self.button5.setObjectName("button5")
        MainWindow.setCentralWidget(self.centralwidget)
        
        ### Tools and Help ###
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 591, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)
        self.actionDocumentation_PDF = QtWidgets.QAction(MainWindow)
        self.actionDocumentation_PDF.setObjectName("actionDocumentation_PDF")
        
        
        self.actionMoodle = QtWidgets.QAction(MainWindow)
        self.actionMoodle.setStatusTip("")
        self.actionMoodle.setObjectName("actionMoodle")
        
        
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.menuHelp.addAction(self.actionDocumentation_PDF)
        self.menuTools.addAction(self.actionClear)
        self.menuTools.addAction(self.actionReset)
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyAutoMark"))
        self.groupBox2.setTitle(_translate("MainWindow", "File selection"))
        self.button1.setStatusTip(_translate("MainWindow", "Select the desired assignment key .py file."))
        self.button1.setText(_translate("MainWindow", "Assignment key"))
        self.label1.setText(_translate("MainWindow", ""))
        self.button2.setStatusTip(_translate("MainWindow", "Select the Moodle zip file containing all submissions for marking."))
        self.button2.setText(_translate("MainWindow", "Moodle zip"))
        self.label2.setText(_translate("MainWindow", ""))
        self.label3.setText(_translate("MainWindow", ""))
        self.button3.setStatusTip(_translate("MainWindow", "Manually select individual zip file submissions for marking."))
        self.button3.setText(_translate("MainWindow", "Assignments"))
        self.groupBox1.setTitle(_translate("MainWindow", "Class selection"))
        self.radioButton1.setStatusTip(_translate("MainWindow", "PyAutoMark will save previously accessed directories specific to CS20."))
        self.radioButton1.setText(_translate("MainWindow", "Computer Science 20"))
        self.radioButton2.setStatusTip(_translate("MainWindow", "PyAutoMark will save previously accessed directories specific to CS30."))
        self.radioButton2.setText(_translate("MainWindow", "Computer Science 30"))
        self.groupBox3.setTitle(_translate("MainWindow", "Program execution and results"))
        self.table1.setSortingEnabled(True)
        item = self.table1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.table1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Grade"))
        self.button6.setStatusTip(_translate("MainWindow", "Choose which .txt file(s) you wish to review."))
        self.button6.setText(_translate("MainWindow", "Open output .txt file directory"))
        self.button4.setStatusTip(_translate("MainWindow", "Initiates the auto-marking process."))
        self.button4.setText(_translate("MainWindow", "Run program"))
        # self.button5.setStatusTip(_translate("MainWindow", "Opens error log text file."))
        # self.button5.setText(_translate("MainWindow", "Error log"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionDocumentation_PDF.setText(_translate("MainWindow", "Documentation (PDF)"))
        self.actionMoodle.setText(_translate("MainWindow", "Process Moodle zip"))
        self.actionClear.setText(_translate("MainWindow", "Clear results"))
        self.actionReset.setText(_translate("MainWindow", "Reset all"))
        
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        # self.button5.setEnabled(False)
        self.button6.setEnabled(False)
        self.label1.setWordWrap(True)
        self.label2.setWordWrap(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

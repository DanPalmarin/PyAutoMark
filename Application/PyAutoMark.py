import sys
import os
import shutil
import json
import zipfile
#import subprocess
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QListWidgetItem
from importlib import import_module, reload
from pathlib import Path

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        super().__init__()
        
        # Main directory (Pyinstaller friendly code)
        if getattr(sys, 'frozen', False):
            self.main_dir = os.path.dirname(sys.executable)
        else:
            self.main_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Read in config settings from config.json
        with open(Path(self.main_dir, 'config.json'), 'r') as f:
            self.config = json.load(f)
            
        # Define key variables
        self.button1_dir = self.config['default_dir1']
        self.button2_dir = self.config['default_dir2']
        self.button1_bool = False
        self.button2_bool = False
        self.checked = [] # this will hold all previously checked zipped file paths
        self.modules = [] # this will hold all previously imported student assignments
        
        # Build the interface
        self.setupUi(MainWindow)
        
        # Define menubar functionality
        self.actionClear.triggered.connect(self.clear_handler)
        self.actionReset.triggered.connect(self.reset_handler)
        self.actionDocumentation_PDF.triggered.connect(self.doc_handler)
        
        # Defining button functionality
        self.button1.clicked.connect(self.button1_handler)
        self.button2.clicked.connect(self.button2_handler)
        self.button3.clicked.connect(self.button3_handler)
        self.button4.clicked.connect(self.button4_handler)
        
        # Define list functionality
        self.list1.itemDoubleClicked.connect(self.list1_handler)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(483, 641)
        
        # Defining each widget and its properties (from QtDesigner)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox1.setGeometry(QtCore.QRect(20, 20, 441, 101))
        self.groupBox1.setObjectName("groupBox1")
        self.button1 = QtWidgets.QPushButton(self.groupBox1)
        self.button1.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.button1.setObjectName("button1")
        self.label1 = QtWidgets.QLabel(self.groupBox1)
        self.label1.setGeometry(QtCore.QRect(110, 24, 321, 27))
        self.label1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label1.setObjectName("label1")
        self.button2 = QtWidgets.QPushButton(self.groupBox1)
        self.button2.setGeometry(QtCore.QRect(10, 60, 91, 31))
        self.button2.setObjectName("button2")
        self.label2 = QtWidgets.QLabel(self.groupBox1)
        self.label2.setGeometry(QtCore.QRect(110, 64, 321, 27))
        self.label2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label2.setObjectName("label2")
        
        self.groupBox2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox2.setGeometry(QtCore.QRect(20, 130, 441, 451))
        self.groupBox2.setObjectName("groupBox2")
        
        
        self.table1 = QtWidgets.QTableWidget(self.groupBox2)
        self.table1.setGeometry(QtCore.QRect(10, 60, 221, 381))
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
        #self.table1.setRowCount(0)
        
        item = QtWidgets.QTableWidgetItem()
        self.table1.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table1.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table1.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.table1.setItem(0, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.table1.setItem(0, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.table1.setItem(1, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.table1.setItem(1, 1, item)
        
        #self.table1.setColumnWidth(1, 40)
        #self.table1.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        #self.table1.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table1.horizontalHeader().setVisible(True)
        self.table1.horizontalHeader().setCascadingSectionResizes(False)
        self.table1.horizontalHeader().setStretchLastSection(True)
        self.table1.verticalHeader().setVisible(True)
        self.table1.verticalHeader().setCascadingSectionResizes(False)
        self.table1.verticalHeader().setHighlightSections(True)
        self.table1.verticalHeader().setSortIndicatorShown(False)
        self.table1.verticalHeader().setStretchLastSection(False)
        
        
        self.list1 = QtWidgets.QListWidget(self.groupBox2)
        self.list1.setGeometry(QtCore.QRect(250, 60, 181, 341))
        #self.list1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list1.setObjectName("list1")
        # item = QtWidgets.QListWidgetItem()
        # self.list1.addItem(item)
        # item = QtWidgets.QListWidgetItem()
        # self.list1.addItem(item)
        self.button4 = QtWidgets.QPushButton(self.groupBox2)
        self.button4.setGeometry(QtCore.QRect(250, 410, 181, 31))
        self.button4.setObjectName("button4")
        self.button3 = QtWidgets.QPushButton(self.groupBox2)
        self.button3.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.button3.setObjectName("button3")
        self.label3 = QtWidgets.QLabel(self.groupBox2)
        self.label3.setGeometry(QtCore.QRect(110, 30, 321, 21))
        self.label3.setObjectName("label3")
        MainWindow.setCentralWidget(self.centralwidget)
        
        ### Tools and Help ###
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 479, 21))
        self.menubar.setObjectName("menubar")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # Clear results tab
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.menuTools.addAction(self.actionClear)
        self.menubar.addAction(self.menuTools.menuAction())
        
        # Reset all tab
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.menuTools.addAction(self.actionReset)
        self.menubar.addAction(self.menuTools.menuAction())
        
        # Documentation tab
        self.actionDocumentation_PDF = QtWidgets.QAction(MainWindow)
        self.actionDocumentation_PDF.setObjectName("actionDocumentation_PDF")
        self.menuHelp.addAction(self.actionDocumentation_PDF)
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyAutoMark"))
        MainWindow.setWindowIcon(QtGui.QIcon(self.main_dir + "\\icon.ico"))
        
        self.groupBox1.setTitle(_translate("MainWindow", "File selection"))
        self.button1.setStatusTip(_translate("MainWindow", "Select the desired assignment key .py file."))
        self.button1.setText(_translate("MainWindow", "Assignment key"))
        self.label1.setText(_translate("MainWindow", ''))
        self.button2.setStatusTip(_translate("MainWindow", "Select the .zip assignment(s) that require marking."))
        self.button2.setText(_translate("MainWindow", "Assignments"))
        self.label2.setText(_translate("MainWindow", ''))
        self.groupBox2.setTitle(_translate("MainWindow", "Program execution and results"))
        self.table1.setSortingEnabled(True)
        # item = self.table1.verticalHeaderItem(0)
        # item.setText(_translate("MainWindow", "1"))
        # item = self.table1.verticalHeaderItem(1)
        # item.setText(_translate("MainWindow", "2"))
        
        item = self.table1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.table1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Grade"))
        __sortingEnabled = self.table1.isSortingEnabled()
        self.table1.setSortingEnabled(False)
        
        #item = self.table1.item(0, 0)
        # item.setText(_translate("MainWindow", "Bob"))
        # item = self.table1.item(0, 1)
        # item.setText(_translate("MainWindow", "10"))
        # item = self.table1.item(1, 0)
        # item.setText(_translate("MainWindow", "Dylan"))
        # item = self.table1.item(1, 1)
        # item.setText(_translate("MainWindow", "8"))
        self.table1.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.list1.isSortingEnabled()
        self.list1.setSortingEnabled(False)
        # item = self.list1.item(0)
        # item.setText(_translate("MainWindow", "Test1"))
        # item = self.list1.item(1)
        # item.setText(_translate("MainWindow", "Test2"))
        self.list1.setSortingEnabled(__sortingEnabled)
        
        # Status tips
        self.button4.setStatusTip(_translate("MainWindow", "Opens the directory that contains the output .txt files."))
        self.button4.setText(_translate("MainWindow", "Open output .txt file directory"))
        self.button3.setStatusTip(_translate("MainWindow", "Initiates the auto-marking process."))
        self.list1.setStatusTip(_translate("MainWindow", "Double-click to open selected .txt file."))
        self.actionClear.setStatusTip(_translate("MainWindow", "Clears table and list data."))
        self.actionReset.setStatusTip(_translate("MainWindow", "Clears table and list data and resets saved directories back to the default."))
        
        self.button3.setText(_translate("MainWindow", "Run program"))
        self.label3.setText(_translate("MainWindow", ""))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionClear.setText(_translate("MainWindow", "Clear results"))
        self.actionReset.setText(_translate("MainWindow", "Reset all"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionDocumentation_PDF.setText(_translate("MainWindow", "Documentation (PDF)"))
        
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.label1.setWordWrap(True)
        self.label2.setWordWrap(True)

    def button1_handler(self):
        filename = QFileDialog.getOpenFileName(None, "Select a solution key (.py).", self.button1_dir, "Python file (*.py)")
        self.button1_file = filename[0]
        self.button1_dir = os.path.dirname(self.button1_file)
        self.button1_basename = os.path.basename(self.button1_file)

        if self.button1_file != "":
            self.label1.setText(self.button1_basename)
            
            file_extension = os.path.splitext(self.button1_file)[1]
            if file_extension == '.py':
                self.button1_bool = True
                
                # update the config file
                path = os.path.dirname(self.button1_file)
                self.config['default_dir1'] = path
                with open('config.json', 'w') as f:
                    json.dump(self.config, f)
            else:
                self.button1_bool = False
        
        if self.button1_bool == True and self.button2_bool == True:
            self.button3.setEnabled(True)
        else:
            self.button3.setEnabled(False)
            
    def button2_handler(self):
        filename = QFileDialog.getOpenFileNames(None, "Select any number of student assignments (.zip).", self.button2_dir, "Zip file(s) (*.zip)")
        self.button2_list = filename[0]
        
        if self.button2_list != []:
            self.button2_dir = os.path.dirname(self.button2_list[0])
            self.button2_bool = True
            for file in self.button2_list:
                file_extension = os.path.splitext(file)[1]
                if file_extension != '.zip':
                    self.button2_bool = False

            if self.button2_bool == True:
                # update the config file
                path = os.path.dirname(self.button2_list[0])
                self.config['default_dir2'] = path
                with open('config.json', 'w') as f:
                    json.dump(self.config, f)
                
                # update label
                self.label2.setText("{0} zip file(s) selected".format(len(self.button2_list)))
        
        if self.button1_bool == True and self.button2_bool == True:
            self.button3.setEnabled(True)
        else:
            self.button3.setEnabled(False)
             
    def button3_handler(self):
        # Display progress
        #self.label3.setText("Auto-marking...")
        
        # Obtain needed paths and import the solution key 
        head, tail = os.path.split(self.button1_file) #store the sol dir and the sol file in separate local variables
        trim_tail = os.path.splitext(tail)[0]
        sys.path.insert(1, head) # places the desired dir in the correct place for import_module below
        solMod = import_module(trim_tail) # variables defined in trim_tail should be referenced as: solMod.variable
        
        # Loop through each zip file in self.button2_list
        self.extracted_dir = Path(self.button2_dir, "Temp_Extracted")
        for zip_file in self.button2_list:
            # we continue to the next zip_file if the current one is in 'checked'
            if zip_file not in self.checked:
                # Determine the student's name from the name of the submitted zip file
                word = zip_file[zip_file.rfind('/')+1:]
                word1 = "A{0}_".format(solMod.assignment_num)
                word2 = word.replace(word1, '')
                student_name = word2.replace('.zip', '')
                
                # Define the output text file for this student
                self.output_dir = Path(self.button2_dir, "Output_Summaries")
                Path(self.output_dir).mkdir(parents=True, exist_ok=True) #checks if output_dir exists - if not, it creates it
                self.output_file = Path(self.output_dir, "{0}{1}{2}".format(word1,student_name,".txt"))
                with open(self.output_file, 'w') as f:
                    f.write("Assignment {0}\n\n".format(solMod.assignment_num))
                      
                # Extract zipped assignment submission
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(self.extracted_dir)
                
                # Running grade total
                self.grade = 0
                NHI = False
                
                # Run each python script in extracted_dir and compare it to the inputs/outputs in solMod.Q_all
                marked_questions = []
                question_numbers = list(range(1,len(solMod.Q_all)+1))
                
                for i in question_numbers:
                    mark = 0 # Initialize the mark that a student gets on a question as 0
                    for entry in os.scandir(self.extracted_dir):
                        if "A{0}_{1}.py".format(solMod.assignment_num, i) in entry.path:
                            marked_questions.append(i)
                            if type(solMod.Q_all[i-1]) is dict:
                                inputs = list(solMod.Q_all[i-1].keys())
                                outputs = list(solMod.Q_all[i-1].values())
                                #call method
                                mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible) 
                            else:
                                inputs = []
                                outputs = [solMod.Q_all[i-1]]
                                #call method
                                mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible)
                            break
                            
                    self.grade += mark
                    
                if question_numbers != marked_questions:
                    unmarked_questions = sorted(list(set(question_numbers) - set(marked_questions)))
                    with open(self.output_file, 'a') as f:
                        output_arg = str(unmarked_questions)[1:-1]
                        f.write("{0}The following questions were not found: {1}.".format(chr(0x002A), output_arg))
                        NHI = True
                
                # Update table heading 'Grade' with the assignment total
                item = self.table1.horizontalHeaderItem(1)
                item.setText("Grade /{0}".format(sum(solMod.Q_weight)))
                
                # Populate the table with the name of the student and his/her grade
                rowPosition = self.table1.rowCount()
                self.table1.insertRow(rowPosition)
                self.table1.setItem(rowPosition,0, QTableWidgetItem(student_name))
                if NHI == True:
                    item = QTableWidgetItem(str(self.grade)+ chr(0x002A))
                else:
                    item = QTableWidgetItem(str(self.grade))
                
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table1.setItem(rowPosition,1, item)
                
                # Populate the list with the name of the output text file
                self.list1.addItem(QListWidgetItem("{0}{1}.txt".format(word1, student_name)))
            
                # Add zip_file to checked if it isn't in already
                self.checked.append(zip_file)
                
                # Detete the 'Temp_Extracted' directory and all of its contents
                if Path(self.extracted_dir).is_dir():
                    shutil.rmtree(self.extracted_dir) # detete the 'Temp_Extracted' directory and all of its contents
        
        self.button4.setEnabled(True)

    def button4_handler(self):
        os.startfile(self.output_dir) # Windows only; this lauches the folder that contains the output .txt files (in explorer)
   
    def list1_handler(self, item):
        os.startfile("{0}\\{1}".format(self.output_dir, item.text())) # Windows only;
    
    def clear_handler(self):
        self.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.list1.clear()
        self.checked = []
    
    def reset_handler(self):
        self.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.list1.clear()
        self.checked = []
        self.config_initialize()
        
        # Read in config settings from config.json
        with open(Path(self.main_dir, 'config.json'), 'r') as f:
            self.config = json.load(f)
            
        # Define key variables
        self.button1_dir = self.config['default_dir1']
        self.button2_dir = self.config['default_dir2']
        
        # Reset labels
        self.label1.setText('')
        self.label2.setText('')
        
        # Disable the bottom two buttons
        self.button1_bool = False
        self.button2_bool = False
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        
    def config_initialize(self):
        config = {"default_dir1": self.main_dir, "default_dir2": self.main_dir} # This resets the default path to the program location
        with open(Path(self.main_dir, 'config.json'), 'w') as f:
            json.dump(config, f)
    
    def doc_handler(self):
        doc = Path(self.main_dir, "PyAutoMark_Documentation.pdf")
        os.startfile(doc)
        #subprocess.Popen([doc],shell=True) # use Popen instead of run, as run requires the pdf to close to continue working in PyAutoMark.
        
    def question(self, Q_num, file, inp, outp, outfile, weight, flexible):
        # Note: The outfile is opened in append mode; all console output is also written outfile.
        head, tail = os.path.split(file.path) #store the sol dir and the sol file in separate local variables
        trim_tail = os.path.splitext(tail)[0]
        sys.path.insert(1, head)
        
        # This is broken into two main types of solutions: (1) No user input is expected; (2) User input is expected.
        # Recall: 'inp' contains the user input from the solution key.
        if inp == []:
            # Properly format the desired output from the solution key (with newlines)
            if type(outp[0]) is tuple:
                formatted_output = self.in_out_with_newlines(outp[0])
            else:
                formatted_output = str(outp[0])
            
            # Capture the result of the submission
            result = self.running_assignments(trim_tail, None)
            
            # For printing out to text files
            print_out = formatted_output.replace("\n", "\\n")
            print_res = str(result).replace("\n", "\\n")
            
            # Report output or errors.
            # If Q_num is in solMod.Q_flexible, then we check only for containment
            if Q_num in flexible:
                if type(outp[0]) is tuple:
                    # If the type is a tuple then we check each element of the tuple for containment in result.
                    containment_check = []
                    for element in outp[0]:
                        containment_check.append(str(element) in result)
                    
                    if False in containment_check:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
                else:
                    # This is the simple case: no newlines should be presented in desired ouput.
                    if formatted_output not in result:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
            else: 
                if result != str(formatted_output): # Checks for strict equality
                    #print("{0}. Incorrect\n      Desired output: {1} \n      Your output: {2}".format(Q_num, outp[0], result.stdout))
                    with open(outfile, 'a') as f:
                        f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, result))
                    return 0
                else:
                    #print("{0}. Correct\n".format(Q_num))
                    with open(outfile, 'a') as f:
                        f.write("{0}. Correct\n\n".format(Q_num))
                    return weight[Q_num-1]
        else:
            success = True
            console_output = []
    
            # We check each list of inputs in 'input' and compare them to the corresponding outputs in 'outputs'.
            for i in range(len(inp)):
                # Properly format the desired output from the solution key (with newlines)
                if type(outp[i]) is tuple:
                    formatted_output = self.in_out_with_newlines(outp[i])
                else:
                    formatted_output = str(outp[i])
                
                # Properly format the input with newlines
                if type(inp[i]) is tuple:
                    formatted_input = self.in_out_with_newlines(inp[i])
                    result = self.running_assignments(trim_tail, formatted_input)
                else:
                    result = self.running_assignments(trim_tail, str(inp[i]))
                
                # For printing out to text files
                print_out = formatted_output.replace("\n", "\\n")
                print_res = str(result).replace("\n", "\\n")
            
                # Report output or errors.
                # If Q_num is in solMod.Q_flexible, then we check only for containment
                if Q_num in flexible:
                    if type(outp[i]) is tuple:
                        # If the type is a tuple then we check each element of the tuple for containment in result.
                        containment_check = []
                        for element in outp[i]:
                            containment_check.append(str(element) in result)
                        
                        if False in containment_check:
                            success = False
                            console_output.append("    -Test {0}: failure\n".format(i+1))
                            console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                        else:
                            if i == len(inp)-1:
                                console_output.append("    -Test {0}: success\n\n".format(i+1))
                            else:
                                console_output.append("    -Test {0}: success\n".format(i+1))
                    else:
                        # This is the simple case: no newlines should be presented in desired ouput.
                        if formatted_output not in result:
                            success = False
                            console_output.append("    -Test {0}: failure\n".format(i+1))
                            console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                        else:
                            if i == len(inp)-1:
                                console_output.append("    -Test {0}: success\n\n".format(i+1))
                            else:
                                console_output.append("    -Test {0}: success\n".format(i+1))
                else:
                    if result != formatted_output: # Checks for strict equality
                        success = False
                        console_output.append("    -Test {0}: failure\n".format(i+1))
                        console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                    else:
                        if i == len(inp)-1:
                            console_output.append("    -Test {0}: success\n\n".format(i+1))
                        else:
                            console_output.append("    -Test {0}: success\n".format(i+1))
            
            if success:
                #print("{0}. Correct".format(Q_num))
                with open(outfile, 'a') as f:
                    f.write("{0}. Correct\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a') as f:
                        f.write(line)
                return weight[Q_num-1]
            else:
                #print("{0}. Incorrect".format(Q_num))
                with open(outfile, 'a') as f:
                    f.write("{0}. Incorrect\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a') as f:
                        f.write(line)
                return 0

    def running_assignments(self, assignment, input_feed):
        output_feed = StringIO()
        with redirect_stdout(output_feed):
            with self.replace_stdin(StringIO(input_feed)):
                if assignment not in self.modules:
                    try:
                        varMod = import_module(assignment)
                        self.modules.append(assignment)
                        res = output_feed.getvalue().rstrip()
                    except Exception as err:
                        res = "Error: {0}".format(err)
                else:
                    try:
                        varMod = import_module(assignment)
                        varMod = reload(varMod)
                        res = output_feed.getvalue().rstrip()
                    except Exception as err:
                        res = "Error: {0}".format(err)
        return res
    
    def in_out_with_newlines(self, some_tuple):
        new_string = ""
        for x in some_tuple:
            temp_entry = "{0}\n".format(x)
            new_string += temp_entry
    
        new_string = new_string.rstrip()
        return new_string
    
    @contextmanager
    def replace_stdin(self, target):
        orig = sys.stdin
        sys.stdin = target
        yield
        sys.stdin = orig





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow) # ui is the interface class
    MainWindow.show()
    sys.exit(app.exec_())

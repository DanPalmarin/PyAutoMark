import sys
import os
import shutil
import json
import zipfile
import threading
import _thread
from pathlib import Path
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from importlib import import_module, reload
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.sip import assign
from main_window import Ui_MainWindow
# import traceback

class Main(QMainWindow):
    def __init__(self):

        self.whitelisted = ["math","_io", "functools", "sys"] # Permitted moduled when executing functions

        # Initialize the main window
        super().__init__()
        
        # Main directory (Pyinstaller friendly code)
        if getattr(sys, 'frozen', False):
            self.main_dir = os.path.dirname(sys.executable)
        else:
            self.main_dir = os.path.dirname(os.path.abspath(__file__))
        
        import_file = Path(self.main_dir + "/imports.txt") # "Imports" all of the modules in imports.txt. It sets them as none in sys.modules
        with open(import_file,"r", encoding="utf-8") as file:
            f = file.read().split("\n")
            for w in f:
                if(w not in sys.modules and w not in self.whitelisted):
                    sys.modules[w] = None
            
        #Build the main window interface from main_window.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Read in config settings from config.json
        try:
            with open(Path(self.main_dir, 'config.json', encoding="utf-8"), 'r') as f:
                self.config = json.load(f)
        except:
            self.config_initialize()
        # Define key variables
        self.CS20button1_dir = self.config['CS20default_dir1']
        self.CS20button2_dir = self.config['CS20default_dir2']
        self.CS20button3_dir = self.config['CS20default_dir3']
        self.CS30button1_dir = self.config['CS30default_dir1']
        self.CS30button2_dir = self.config['CS30default_dir2']
        self.CS30button3_dir = self.config['CS30default_dir3']
        self.button1_bool = False
        self.button2_bool = False
        self.button3_bool = False
        self.checked = [] # this will hold all previously checked zipped file paths
        self.modules = [] # this will hold all previously imported student assignments
        
        # Define menubar functionality
        self.ui.actionClear.triggered.connect(self.clear_handler)
        self.ui.actionReset.triggered.connect(self.reset_handler)
        self.ui.actionDocumentation_PDF.triggered.connect(self.doc_handler)
        
        # Define radio button functionality (Class Selection)
        self.ui.radioButton1.toggled.connect(self.radioButton_handler)
        self.ui.radioButton2.toggled.connect(self.radioButton_handler)
        
        # Defining button functionality
        ## File Selection
        self.ui.button1.clicked.connect(self.button1_handler)
        self.ui.button2.clicked.connect(self.button2_handler)
        self.ui.button3.clicked.connect(self.button3_handler)
        ## Program Execution
        self.ui.button4.clicked.connect(self.button4_handler)
        #self.ui.button5.clicked.connect(self.button5_handler)
        self.ui.button6.clicked.connect(self.button6_handler)
        
        # Define list functionality
        self.ui.list1.itemDoubleClicked.connect(self.list1_handler)
        
    def radioButton_handler(self, b):
        self.ui.button1.setEnabled(True)
        self.ui.button2.setEnabled(True)
        self.ui.button3.setEnabled(True)
    
    # Select answer key
    def button1_handler(self):
        if self.ui.radioButton1.isChecked():
            filename = QFileDialog.getOpenFileName(None, "Select a solution key (.py).", self.CS20button1_dir, "Python file (*.py)") #returns as tuple: (path, type)
        elif self.ui.radioButton2.isChecked():
            filename = QFileDialog.getOpenFileName(None, "Select a solution key (.py).", self.CS30button1_dir, "Python file (*.py)") #returns as tuple: (path, type)
            
        self.button1_file = filename[0]
        self.button1_basename = os.path.basename(self.button1_file)

        if self.button1_file != "":
            # update label
            self.ui.label1.setText(self.button1_basename)
            self.button1_bool = True
            
            # update the config file
            path = os.path.dirname(self.button1_file)
            if self.ui.radioButton1.isChecked():
                self.config['CS20default_dir1'] = path
            if self.ui.radioButton2.isChecked():
                self.config['CS30default_dir1'] = path
            
            with open('config.json', 'w', encoding="utf-8") as f:
                    json.dump(self.config, f)
            
            # update the CS20button1_dir with the user selected directory
            self.CS20button1_dir = os.path.dirname(self.button1_file)
        else:
            self.button1_bool = False
            self.ui.label1.setText("")
        
        # decides when to enable the "Run program" button
        if self.button1_bool == True and self.button2_bool == True or self.button1_bool == True and self.button3_bool == True:
            self.ui.button4.setEnabled(True)
        else:
            self.ui.button4.setEnabled(False)
    
    # Select Moodle zip
    def button2_handler(self):
        if self.ui.radioButton1.isChecked():
            self.moodle_zip = QFileDialog.getOpenFileName(None, "Select a single Moodle zip file (.zip).", self.CS20button2_dir, "Zip file (*.zip)")[0]
        elif self.ui.radioButton2.isChecked():
            self.moodle_zip = QFileDialog.getOpenFileName(None, "Select a single Moodle zip file (.zip).", self.CS30button2_dir, "Zip file (*.zip)")[0]
        
        self.moodle_zip_file = Path(self.moodle_zip)
        self.moodle_dir = Path(self.moodle_zip).resolve().parent # directory of the moodle zip
        self.moodle_name = Path(self.moodle_zip).stem # basename of the moodle zip
        self.new_moodle_dir = Path(self.moodle_dir, self.moodle_name) # directory of the future uncompressed Moodle zip
        
        # update the button label
        if self.moodle_zip != "":
            # update the config file
            path = os.path.dirname(self.moodle_zip_file)
            if self.ui.radioButton1.isChecked():
                self.config['CS20default_dir2'] = path
            elif self.ui.radioButton2.isChecked():
                self.config['CS30default_dir2'] = path
            
            with open('config.json', 'w', encoding="utf-8") as f:
                    json.dump(self.config, f)
            
            # update the CS20button2_dir with the user selected directory
            self.CS20button2_dir = os.path.dirname(self.moodle_zip)
            
            # counts the number of zip files in the Moodle zip
            zip_file = zipfile.ZipFile(self.moodle_zip_file, 'r')
            zip_file_num = 0
            for file in zip_file.namelist():
                zip_file_num += 1
                
            self.ui.label2.setText("{0} zip file(s) contained.".format(zip_file_num))
            self.button2_bool = True
            self.ui.button3.setEnabled(False)
        else:
            self.ui.label2.setText("")
            self.button2_bool = False
            self.ui.button3.setEnabled(True)
        
        # decides when to enable the "Run program" button
        if self.button1_bool == True and self.button2_bool == True or self.button1_bool == True and self.button3_bool == True:
            self.ui.button4.setEnabled(True)
        else:
            self.ui.button4.setEnabled(False)
        
    # Select assignments
    def button3_handler(self):
        if self.ui.radioButton1.isChecked():
            filename = QFileDialog.getOpenFileNames(None, "Select any number of student assignments (.zip).", self.CS20button3_dir, "Zip file(s) (*.zip)") #returns as tuple: (path, type)
        elif self.ui.radioButton2.isChecked():
            filename = QFileDialog.getOpenFileNames(None, "Select any number of student assignments (.zip).", self.CS30button3_dir, "Zip file(s) (*.zip)") #returns as tuple: (path, type)
        
        self.button3_list = filename[0]
        
        if self.button3_list != []:
            # update label
            self.ui.label3.setText("{0} zip file(s) selected.".format(len(self.button3_list)))
            self.button3_bool = True
            
            self.CS20button3_dir = os.path.dirname(self.button3_list[0]) # used in button4_handler
            
            # update the config file
            path = os.path.dirname(self.button3_list[0])
            if self.ui.radioButton1.isChecked():
                self.config['CS20default_dir3'] = path
            elif self.ui.radioButton2.isChecked():
                self.config['CS30default_dir3'] = path
            
            with open('config.json', 'w', encoding="utf-8") as f:
                json.dump(self.config, f)
            
            # # update the CS20button3_dir with the user selected directory
            # self.CS20button3_dir = os.path.dirname(self.button3_list)
        else:
            self.button3_bool = False
            self.ui.label3.setText("")
            
        # decides when to enable the "Run program" button
        if self.button1_bool == True and self.button2_bool == True or self.button1_bool == True and self.button3_bool == True:
            self.ui.button4.setEnabled(True)
        else:
            self.ui.button4.setEnabled(False)
        
    # Run programs
    def button4_handler(self):
        # Obtain needed paths and import the solution key 
        head, tail = os.path.split(self.button1_file) #store the sol dir and the sol file in separate local variables
        trim_tail = os.path.splitext(tail)[0]
        sys.path.insert(1, head) # places the desired dir in the correct place for import_module below
        solMod = import_module(trim_tail) # variables defined in trim_tail should be referenced as: solMod.variable
        
        # Turn off sorting to avoid conflicts
        self.ui.table1.setSortingEnabled(False)

        # If Moodle zip was used, we extract the files to the "Student_Submissions" folder contained in the directory with the Moodle zip.
        # We then loop through each zipped submission.
        # If "Assignments" button was used, we loop through each zip file in self.button3_list.
        
        if self.button2_bool == True:
            # Checks if Student_Submissions folder exists - if not, it creates it in the directory that contains the Moodle zip
            zipped_submissions = Path(self.moodle_dir, "Student_Submissions")
            Path(zipped_submissions).mkdir(parents=True, exist_ok=True)

            # Extract the zipped Moodle file to self.new_moodle_dir
            with zipfile.ZipFile(self.moodle_zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.new_moodle_dir)

            # Iterate over each folder in "Student_Submissions"
            # moodle_zips_list will hold on to each student zipped submission (still zipped) with a newly formatted name.
            moodle_zips_list = []
            for entry in os.scandir(self.new_moodle_dir):
                # We prep future file for a single feedback file zip (following Moodle's formatting).
                # We need the name of each folder to be the name of each corresponding zip file inside each folder.
                full_moodle_name = entry.name
                for A_name_zip in Path(entry).iterdir(): # There should only be 1 zip file here
                    extension = os.path.splitext(A_name_zip)[1]
                    new_name = Path(full_moodle_name + extension)
                    shutil.move(A_name_zip, zipped_submissions.joinpath(new_name)) # Moves each file to "Student_Submissions" folder and replaces files if they already exist.
                    moodle_zips_list.append(str(Path(A_name_zip, zipped_submissions, new_name))) # Add new zipped file locations to a list to be iterated over later.
            
            # Delete the self.new_moodle_dir and all of its contents
            if Path(self.new_moodle_dir).is_dir():
                shutil.rmtree(self.new_moodle_dir)
            
            # We loop through each zip file in "Student_Submissions" and mark it.
            self.extracted_dir = Path(zipped_submissions, "Temp_Extracted")
            for zip_file in moodle_zips_list:
                # we continue to the next zip_file if the current one is in 'checked'
                if zip_file not in self.checked:
                    # Bulk moodle download file format: 'firstname lastname_ID#_assignsubmission_file_.zip' - set by Moodle
                    file_name = Path(zip_file).stem # returns the basename of the zip_file
                    
                    #When the moodle zip is selected, it's nice to report the student names as "last, first", to match Aspen.
                    student_name = file_name[:file_name.find('_')]
                    student_name = student_name.split()
                    student_name = "{}, {}".format(student_name[1], student_name[0])
                    
                    #We make a version of student_name without "-" or ", ", so that the file name is safe when we import them as modules.
                    safe_student_name = student_name.replace(", ", "")
                    safe_student_name = safe_student_name.replace("-", "")
                    
                    # Initialize the output text file.
                    # Define the output text file for this student
                    self.output_dir = Path(zipped_submissions, "Output_Summaries")
                    Path(self.output_dir).mkdir(parents=True, exist_ok=True) #checks if output_dir exists - if not, it creates it
                    
                    # If the zip_file is from a bulk moodle download, the name must be file_name for easy feedback dump.
                    self.output_file = Path(self.output_dir, "{0}{1}".format(file_name,".txt"))
                    with open(self.output_file, 'w', encoding="utf-8") as f:
                        f.write("Assignment {0}\n\n".format(solMod.assignment_num))
                    
                    lastdir = os.getcwd()
                    # Extract zipped assignment submission while checking for if it is zipped incorrectly
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(self.extracted_dir)
                        os.chdir(self.extracted_dir)
                        for f in os.listdir(self.extracted_dir):
                            if(os.path.isdir(f)):
                                os.chdir(f)
                                for file in os.listdir():
                                    shutil.copy(file,self.extracted_dir)
                    os.chdir(lastdir)
                    
                    # Get all possible names for each question
                    legal_questions = []
                    for x in range(1,len(solMod.Q_all) + 1):
                        legal_questions.append(f"A{solMod.assignment_num}_{x}")

                    ### Change name of each A#_# to be A#_#NAME so that each module is unique.
                    # for entry in os.scandir(self.extracted_dir):
                        # ### Here's where we append the student name to the file name so that each imported script is unique (to avoid builtin function overwrite errors)
                        # old_entry = Path(entry.path) # Full path to .py file as a string.
                        # entry_dir = old_entry.parent # C:\Users\USERNAME\some_directories\Temp_Extracted
                        # old_entry_tail = old_entry.stem # A#_#
                        # entry_ext = old_entry.suffix # .py extension
                        # if(entry_ext == ".py" and old_entry_tail in legal_questions):
                            # new_entry = "{}\{}{}{}".format(entry_dir, old_entry_tail, safe_student_name, entry_ext) #Full_dir\Temp_Extracted\A#_#NAME.py
                            # new_entry = Path(new_entry)
                            # new_entry_tail = new_entry.stem # A#_#NAME
                            # # os.rename(old_entry, new_entry) #rename the current .py file
                    
                    # Running grade total
                    self.grade = 0
                    NHI = False
                    
                    # Run each python script in extracted_dir and compare it to the inputs/outputs in solMod.Q_all
                    marked_questions = []
                    question_numbers = list(range(1,len(solMod.Q_all)+1))
                    
                    for i in question_numbers:
                        mark = 0 # Initialize the mark that a student gets on a question as 0
                        for entry in os.scandir(self.extracted_dir):
                            #if "A{0}_{1}{2}.py".format(solMod.assignment_num, i, safe_student_name) in entry.path:
                            if "A{0}_{1}.py".format(solMod.assignment_num, i) in entry.path:
                                marked_questions.append(i)
                                
                                if type(solMod.Q_all[i-1]) is dict:
                                    inputs = list(solMod.Q_all[i-1].keys())
                                    outputs = list(solMod.Q_all[i-1].values())
                                    #call method
                                    mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible) 
                                    #mark = self.question(i, new_entry, entry_dir, new_entry_tail, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible) 
                                else:
                                    inputs = []
                                    outputs = [solMod.Q_all[i-1]]
                                    #call method
                                    mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible) 
                                    # mark = self.question(i, new_entry, entry_dir, new_entry_tail, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible)
                                break
                                
                        self.grade += mark
                        
                    if question_numbers != marked_questions:
                        unmarked_questions = sorted(list(set(question_numbers) - set(marked_questions)))
                        with open(self.output_file, 'a', encoding="utf-8") as f:
                            output_arg = str(unmarked_questions)[1:-1]
                            f.write("{0}The following questions were not found: {1}.".format(chr(0x002A), output_arg))
                            NHI = True
                    
                    # Update table heading 'Grade' with the assignment total
                    item = self.ui.table1.horizontalHeaderItem(1)
                    item.setText("Grade /{0}".format(sum(solMod.Q_weight)))
                    
                    # Populate the table with the name of the student and his/her grade
                    rowPosition = self.ui.table1.rowCount()
                    self.ui.table1.insertRow(rowPosition)
                    self.ui.table1.setItem(rowPosition,0, QTableWidgetItem(student_name))
                    if NHI == True:
                        item = QTableWidgetItem(str(self.grade)+ chr(0x002A))
                    else:
                        item = QTableWidgetItem(str(self.grade))
                    
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.table1.setItem(rowPosition,1, item)

                    # Populate the list with the name of the output text file
                    self.ui.list1.addItem(QListWidgetItem("{0}.txt".format(file_name)))
                    #self.ui.list1.addItem(QListWidgetItem("{0}{1}.txt".format(word1, student_name)))
                
                    # Add zip_file to checked if it isn't in already
                    self.checked.append(zip_file)
                    
                    # Delete the 'Temp_Extracted' directory and all of its contents
                    if Path(self.extracted_dir).is_dir():
                        shutil.rmtree(self.extracted_dir) # delete the 'Temp_Extracted' directory and all of its contents
                    
            
            # Add each feedback text file to feedback_zip.
            feedback_zip = zipfile.ZipFile(Path(self.output_dir, "Feedback_Files.zip"), 'w')
            for feedback_file in os.listdir(self.output_dir):
                if feedback_file.endswith(".txt"):
                    feedback_zip.write(Path(self.output_dir, feedback_file), feedback_file)
            feedback_zip.close()
            
            self.ui.button6.setEnabled(True)
            self.ui.table1.setSortingEnabled(True)
            
        elif self.button3_bool == True:
            # Loop through each zip file in self.button3_list
            self.extracted_dir = Path(self.CS20button3_dir, "Temp_Extracted")
            for zip_file in self.button3_list:
                # we continue to the next zip_file if the current one is in 'checked'
                if zip_file not in self.checked:
                    # First, we determine if the zip_file was a bulk moodle download (manually extracted) or an individual moodle download.
                    # Bulk moodle download file format: 'firstname lastname_ID#_assignsubmission_file_.zip' - set by Moodle
                    # Individual moodle download file format: 'A#_firstname.zip' - set by me
                    keyword = "A{0}_".format(solMod.assignment_num) # from solution key
                    file_name = Path(zip_file).stem # returns the basename of the zip_file
                    if keyword in file_name:
                        student_name = file_name.replace(keyword,'')
                    else:
                        student_name = file_name[:file_name.find('_')]
                    
                    #We make a version of student_name without "-" or ", ", so that the file name is safe when we import them as modules.
                    safe_student_name = student_name.replace(", ", "")
                    safe_student_name = safe_student_name.replace("-", "")
                    
                    # Initialize the output text file.
                    # Define the output text file for this student
                    self.output_dir = Path(self.CS20button3_dir, "Output_Summaries")
                    Path(self.output_dir).mkdir(parents=True, exist_ok=True) #checks if output_dir exists - if not, it creates it
                    
                    # If the zip_file is from a bulk moodle download, the name must be file_name for easy feedback dump.
                    #self.output_file = Path(self.output_dir, "{0}{1}{2}".format(word1,student_name,".txt"))
                    self.output_file = Path(self.output_dir, "{0}{1}".format(file_name,".txt"))
                    with open(self.output_file, 'w', encoding="utf-8") as f:
                        f.write("Assignment {0}\n\n".format(solMod.assignment_num))

                    lastdir = os.getcwd()
                    # Extract zipped assignment submission while checking for if it is zipped incorrectly
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(self.extracted_dir)
                        os.chdir(self.extracted_dir)
                        for f in os.listdir(self.extracted_dir):
                            if(os.path.isdir(f)):
                                os.chdir(f)
                                for file in os.listdir():
                                    shutil.copy(file,self.extracted_dir)
                    os.chdir(lastdir)
                    
                    # Get all possible names for each question
                    legal_questions = []
                    for x in range(1,len(solMod.Q_all) + 1):
                        legal_questions.append(f"A{solMod.assignment_num}_{x}")
                    
                    ### Change name of each A#_# to be A#_#NAME so that each module is unique.
                    # for entry in os.scandir(self.extracted_dir):
                        # ### Here's where we append the student name to the file name so that each imported script is unique (to avoid builtin function overwrite errors)
                        # old_entry = Path(entry.path) # Full path to .py file as a string.
                        # entry_dir = old_entry.parent # C:\Users\USERNAME\some_directories\Temp_Extracted
                        # old_entry_tail = old_entry.stem # A#_#
                        # entry_ext = old_entry.suffix # .py extension
                        # if(entry_ext == ".py" and old_entry_tail in legal_questions):
                            # new_entry = "{}\{}{}{}".format(entry_dir, old_entry_tail, safe_student_name, entry_ext) #Full_dir\Temp_Extracted\A#_#NAME.py
                            # new_entry = Path(new_entry)
                            # new_entry_tail = new_entry.stem # A#_#NAME
                            # # os.rename(old_entry, new_entry) #rename the current .py file
                    
                    # Running grade total
                    self.grade = 0
                    NHI = False
                    
                    # Run each python script in extracted_dir and compare it to the inputs/outputs in solMod.Q_all
                    marked_questions = []
                    question_numbers = list(range(1,len(solMod.Q_all)+1))
                    
                    for i in question_numbers:
                        mark = 0 # Initialize the mark that a student gets on a question as 0
                        for entry in os.scandir(self.extracted_dir):
                            #if "A{0}_{1}{2}.py".format(solMod.assignment_num, i, safe_student_name) in entry.path:
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
                        with open(self.output_file, 'a', encoding="utf-8") as f:
                            output_arg = str(unmarked_questions)[1:-1]
                            f.write("{0}The following questions were not found: {1}.".format(chr(0x002A), output_arg))
                            NHI = True
                    
                    # Update table heading 'Grade' with the assignment total
                    item = self.ui.table1.horizontalHeaderItem(1)
                    item.setText("Grade /{0}".format(sum(solMod.Q_weight)))
                    
                    # Populate the table with the name of the student and his/her grade
                    rowPosition = self.ui.table1.rowCount()
                    self.ui.table1.insertRow(rowPosition)
                    self.ui.table1.setItem(rowPosition,0, QTableWidgetItem(student_name))
                    if NHI == True:
                        item = QTableWidgetItem(str(self.grade)+ chr(0x002A))
                    else:
                        item = QTableWidgetItem(str(self.grade))
                    
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.table1.setItem(rowPosition,1, item)
                    
                    # Populate the list with the name of the output text file
                    self.ui.list1.addItem(QListWidgetItem("{0}.txt".format(file_name)))
                    #self.ui.list1.addItem(QListWidgetItem("{0}{1}.txt".format(word1, student_name)))
                
                    # Add zip_file to checked if it isn't in already
                    self.checked.append(zip_file)
                    
                    # Detete the 'Temp_Extracted' directory and all of its contents
                    if Path(self.extracted_dir).is_dir():
                        shutil.rmtree(self.extracted_dir) # detete the 'Temp_Extracted' directory and all of its contents
            
            self.ui.button6.setEnabled(True)
            self.ui.table1.setSortingEnabled(True)

    # Output Directory
    def button6_handler(self):
        os.startfile(self.output_dir) # Windows only; this lauches the folder that contains the output .txt files (in explorer)
   
    def list1_handler(self, item):
        os.startfile("{0}\\{1}".format(self.output_dir, item.text())) # Windows only;

    def clear_handler(self):
        self.ui.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.ui.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.ui.list1.clear()
        self.checked = []
    
    def reset_handler(self):
        self.ui.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.ui.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.ui.list1.clear()
        self.checked = []
        self.config_initialize()
        
        # Read in config settings from config.json
        with open(Path(self.main_dir, 'config.json', encoding="utf-8"), 'r') as f:
            self.config = json.load(f)
            
        # Define key variables
        self.CS20button1_dir = self.config['CS20default_dir1']
        self.CS20button2_dir = self.config['CS20default_dir2']
        self.CS20button3_dir = self.config['CS20default_dir3']
        self.CS30button1_dir = self.config['CS30default_dir1']
        self.CS30button2_dir = self.config['CS30default_dir2']
        self.CS30button3_dir = self.config['CS30default_dir3']
        
        # Reset labels
        self.ui.label1.setText('')
        self.ui.label2.setText('')
        self.ui.label3.setText('')
        
        # Disable the bottom three buttons
        self.ui.button1_bool = False
        self.ui.button2_bool = False
        self.ui.button3_bool = False
        self.ui.button4.setEnabled(False)
        # self.ui.button5.setEnabled(False)
        self.ui.button6.setEnabled(False)
        
    def config_initialize(self):
        # This resets the default paths to the program location
        config = {
        "CS20default_dir1": self.main_dir, 
        "CS20default_dir2": self.main_dir, 
        "CS20default_dir3": self.main_dir,
        "CS30default_dir1": self.main_dir, 
        "CS30default_dir2": self.main_dir, 
        "CS30default_dir3": self.main_dir
        } 
        with open(Path(self.main_dir, 'config.json', encoding="utf-8"), 'w') as f:
            json.dump(config, f)
        self.config = config
    
    def doc_handler(self):
        doc = Path(self.main_dir, "PyAutoMark_Documentation.pdf")
        os.startfile(doc)
        
    #def question(self, Q_num, file, head, trim_tail, inp, outp, outfile, weight, flexible):
    def question(self, Q_num, file, inp, outp, outfile, weight, flexible):
        # Note: The outfile is opened in append mode; all console output is also written to the outfile.
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
            print_out = formatted_output.replace("\n", "   ")
            print_res = str(result).replace("\n", "   ")
            #print_out = formatted_output.replace("\n", "\\n")
            #print_res = str(result).replace("\n", "\\n")
            
            # Report output or errors.
            # If Q_num is in solMod.Q_flexible, then we check only for containment.
            # We also lower case both the key and the submission when checking if flexible.
            if Q_num in flexible:
                if type(outp[0]) is tuple:
                    # If the type is a tuple then we check each element of the tuple for containment in result.
                    containment_check = []
                    for element in outp[0]:
                        containment_check.append(str(element).strip().lower() in result.strip().lower()) #holds True or False (lower case all and remove leading and ending spaces)
                    
                    if True in containment_check: # only require one True for a success
                        with open(outfile, 'a', encoding="utf-8") as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a', encoding="utf-8") as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
                else:
                    # This is the simple case: no newlines should be presented in desired ouput.
                    # Again, if flexible, then everything is lower cased.
                    if formatted_output.strip().lower() not in result.strip().lower():
                        with open(outfile, 'a', encoding="utf-8") as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a', encoding="utf-8") as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
            else: 
                if result != str(formatted_output): # Checks for strict equality
                    #print("{0}. Incorrect\n      Desired output: {1} \n      Your output: {2}".format(Q_num, outp[0], result.stdout))
                    with open(outfile, 'a', encoding="utf-8") as f:
                        f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, result))
                    return 0
                else:
                    #print("{0}. Correct\n".format(Q_num))
                    with open(outfile, 'a', encoding="utf-8") as f:
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
                print_out = formatted_output.replace("\n", "   ")
                print_res = str(result).replace("\n", "   ")
                #print_out = formatted_output.replace("\n", "\\n")
                #print_res = str(result).replace("\n", "\\n")
            
                # Report output or errors.
                # If Q_num is in solMod.Q_flexible, then we check only for containment
                if Q_num in flexible:
                    if type(outp[i]) is tuple:
                        # If the type is a tuple then we check each element of the tuple for containment in result.
                        # We also lower case both the key and the submission when checking if flexible.
                        containment_check = []
                        for element in outp[i]:
                            containment_check.append(str(element).strip().lower() in result.strip().lower())
                        
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
                        # We also lower case both the key and the submission when checking if flexible.
                        if formatted_output.strip().lower() not in result.strip().lower():
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
                with open(outfile, 'a', encoding="utf-8") as f:
                    f.write("{0}. Correct\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a', encoding="utf-8") as f:
                        f.write(line)
                return weight[Q_num-1]
            else:
                #print("{0}. Incorrect".format(Q_num))
                with open(outfile, 'a', encoding="utf-8") as f:
                    f.write("{0}. Incorrect\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a', encoding="utf-8") as f:
                        f.write(line)
                return 0

    # Code derived from https://www.generacodice.com/en/articolo/170539/how-to-limit-execution-time-of-a-function-call-in-python
    @contextmanager
    def time_limit(self, seconds):
        # Start a timer
        timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
        timer.start()
        try:
            yield
        except KeyboardInterrupt:
            raise TimeoutError("Timeout")
        finally:
            # if the action ends in specified time, timer is canceled
            timer.cancel()

    def run(self, assignment, input_feed):
        output_feed = StringIO()
        #print(assignment, self.modules)
        with redirect_stdout(output_feed):
            with self.replace_stdin(StringIO(input_feed)):
                if assignment not in self.modules:
                    for x in sys.modules:# Clear all modules
                        if(x in self.whitelisted):
                            continue
                        sys.modules[x] = None
                    sys.path = [self.extracted_dir.as_posix()] # Empty import paths (removes access to pip installed packages)
                    
                    ####
                    # Removes some built in functions. Not fully isolated, 
                    # but it's good enough that someone would have to really try to get out of the sandbox
                    functions = Path(self.main_dir,"functions.py")
                    functions_temp = Path(self.extracted_dir, assignment + ".py")
                    
                    assignment_file = Path(self.extracted_dir, assignment + ".py")
                    shutil.copy(assignment_file, assignment_file.as_posix() + "___") # Backup student script

                    shutil.copy(functions, functions_temp)
                    tempMod = import_module(assignment) # Importing script to overwrite builtin functions (open, exec, etc.)
                    shutil.copy(assignment_file.as_posix() + "___", assignment_file)

                    reload(tempMod)
                    #replace with varMod = import_module(assignment)
                    ####
                    
                    
                    #self.modules.append(assignment)
                    res = output_feed.getvalue().rstrip()
                #else:
                #    varMod = import_module(assignment)
                #    varMod = reload(varMod)
                #    res = output_feed.getvalue().rstrip()
        return res
    def running_assignments(self, assignment, input_feed):
        #Keep copy of currently imported modules to ignore any modules that are imported by user programs
        temp_modules = sys.modules.copy()
        temp_import_paths = sys.path.copy()
        # sys.path = [] # clear imports
        # sys.modules = []
        try:
            with self.time_limit(1):
                res = self.run(assignment,input_feed)
        except SystemExit:
            res = "Please don't use exit() or sys.exit(). They are useful for the interactive interpreter shell but should not be used in programs."
        except KeyboardInterrupt as err:
            res = "Error: {0}".format(err)
        except GeneratorExit as err:
            res = "Error: {0}".format(err)
        except TimeoutError:
            res = "Error: Program exceeded time limit. Possible infinite loop."
        except Exception as err:
            res = "Error: {0}".format(err)
            # res = "Error: {0}".format(traceback.format_exc())
        #print(set(temp_modules).symmetric_difference(set(sys.modules)))
        sys.modules = temp_modules.copy()
        sys.path = temp_import_paths.copy()
        #try:
        #    sys.modules.pop("chessmoves")
        #except:
        #    pass
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



if __name__ == '__main__':
    #import os
    #os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    
    # # Handle high resolution displays:
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    #app.setStyle("Windowsvista")
    app.setStyle("Fusion")
    w = Main()
    w.show()
    sys.exit(app.exec_())
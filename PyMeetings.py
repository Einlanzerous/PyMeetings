from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QLabel, QLineEdit, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from PyQt5.QtCore import Qt
import sys, csv, datetime
from datetime import date
"""
PyMeetings, a simple Python App using PyQt5 GUI
Records attendance and sends the resulting file to the listed person below
Version 0.45.0

CREATED BY ASHLEY DODSON
August 2017

Future improvements: Change layout to QForm/QGrid, so that resizing works
"""
class Attend(QWidget):    
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        

    # Really need to move the PyQt5 UI off absolute and allow for input on users
    # CB objects are the checkboxes. Lbl are labels for text    
    def initUI(self):
        # Declare variables- attached to the 'self' object
        self.version = "0.45.0"
        self.missing = 0
        self.xloc = 20
        self.yloc = 15
        self.submitted = False
        self.users = {}
        self.total_users = {}

        # Rows for users
        list_of_users = "" # Insert csv file with all users listed. Use, "Users" as header
        self.populated_list = csv.DictReader(open(list_of_users))
        for all in self.populated_list:
            self.total_users[all['Users']] = all['Users']
        
        # These for loops populate the users, but will be merged into a single for loop in the future
        for each in self.total_users:
            self.users[each] = QCheckBox(each, self)
            self.users[each].move(self.yloc, self.xloc)
            self.users[each].toggle()
            self.users[each].stateChanged.connect(self.query)
            self.users[each].setToolTip("Checked box means present, unchecked means absent")

            self.xloc = self.xloc + 20

            if (self.xloc % 160 == 0):
                self.xloc = 20
                self.yloc = self.yloc + 110          

        # Lays out basic UI
        self.bckgrd = QLabel(self)
        picture = QPixmap("") # Insert logo here for team or company
        self.bckgrd.setPixmap(picture)
        self.bckgrd.move(15, 180)
        self.bckgrd.setFixedWidth(250)

        self.bckgrd2 = QLabel(self)
        picture2 = QPixmap("Help_Icon.png")
        self.bckgrd2.setPixmap(picture2)
        self.bckgrd2.move(250, 228)
        self.bckgrd2.setFixedWidth(75)
        self.bckgrd2.setToolTip("Version " + self.version + " created by Ashley Dodson")
        
        self.lbl = QLabel("Total Number of missing persons is " + str(self.missing) + ".", self)
        self.lbl.move(235, 212)
        self.lbl.setFixedWidth(200)

        self.lbl2 = QLabel("<b>Attendees</b>", self)
        self.lbl2.move(75, 5)

        self.lbl3 = QLabel("", self)
        self.lbl3.move(257, 260)
        self.lbl3.setFixedWidth(200)

        submitButton = QPushButton('Submit', self)
        submitButton.setToolTip("This will generate attendance and send the report to named person")
        submitButton.move(335, 233)
        submitButton.clicked.connect(self.submit)
        
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.white)

        self.setWindowIcon(QIcon('Pymeeting_Icon.png'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.setGeometry(350, 350, 425, 300)
        self.setWindowTitle('IT Meeting Attendance')
        self.show()
                
    
    # This part just keeps up with the number of missing employess via the variable missing    
    def query(self, state):      
        if state == Qt.Checked:
            self.missing = self.missing - 1
            self.lbl.setText("Total Number of missing persons is " + str(self.missing) + ".")
        else:
            self.missing = self.missing + 1
            self.lbl.setText("Total Number of missing persons is " + str(self.missing) + ".")


    # This is the button that replaces or creates a file with the attendance generated. Powershell does the transmitting
    def submit(self):
        self.submitted = True
        fileName = "IT_Meeting.txt"
        fileLocation = "" #Insert location of file here, doesn't need filename
        
        file = open(fileLocation + fileName, "w")
        file.write("IT Meeting: " + str(date.today()) + "\n")

        for each in self.total_users:
            if (self.users[each].checkState() == 2):
                present = "Here"
            else:
                present = "Absent"

            file.write("" + each + " is: " + present + "\n")
        
        file.close()

        self.now = datetime.datetime.now()
        self.lbl3.setText("<i>Submitted " + str(self.now.strftime("%m-%d-%Y %H:%M:%S")) + "</i>")
            

# This is kind of what actually launches the program        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Attend()
    sys.exit(app.exec_())

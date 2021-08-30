import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

class Info(QDialog):
    def __init__(self):
        super(Info, self).__init__()
        loadUi("PersonalInfo.ui", self)
        self.pushButton.clicked.connect(self.Start)
        self.pushButton.clicked.connect(self.accept)
        self.IDArray = []
        connection = sqlite3.connect("DataBase.db")
        cur = connection.cursor()
        sqlID = "SELECT * FROM Info LIMIT 10000"
        for row in cur.execute(sqlID):
            self.IDArray.append(row[0])

    def Start(self):
        widget.setCurrentIndex(1)
        widget.setFixedWidth(755)
        widget.setFixedHeight(578)

    def accept(self):
        Data = sqlite3.connect("DataBase.db")
        cur = Data.cursor()
        First = self.lineEdit.text()
        Second = self.lineEdit1.text()
        Third = self.lineEdit2.text()
        Forth = self.label4.text()
        sqlCommand = "INSERT INTO Info(FirstName, LastName, Age, Score) VALUES('"+First+"', '"+Second+"', '"+Third+"', '"+Forth+"');"
        Data.execute(sqlCommand)
        Data.commit()
        Data.close()

class Quiz(QDialog):
    def __init__(self):
        super(Quiz, self).__init__()
        loadUi("PythonQuiz.ui", self)
        self.NEXT.clicked.connect(self.GoNext)
        self.PREVIOUS.clicked.connect(self.GoPrevious)
        self.PhotoArray = ["Pictures/L0.jpg", "Pictures/L1.jpg", "Pictures/L2.jpg", "Pictures/L3.jpg", "Pictures/L4.jpg",
                           "Pictures/L5.jpg", "Pictures/L6.jpg", "Pictures/L7.jpg", "Pictures/L8.jpg", "Pictures/L9.jpg",
                           "Pictures/L10.jpg", "Pictures/L11.jpg", "Pictures/L12.jpg", "Pictures/L13.jpg",
                           "Pictures/L14.jpg", "Pictures/L15.jpg", "Pictures/L16.jpg", "Pictures/L17.jpg",
                           "Pictures/L18.jpg", "Pictures/L19.jpg", "Pictures/L20.jpg", "Pictures/L21.jpg",
                           "Pictures/L22.jpg", "Pictures/L23.jpg", "Pictures/L24.jpg", "Pictures/L25.jpg",
                           "Pictures/L26.jpg"]

        self.score = 0
        self.currentPic = 0
        self.G1 = []
        self.G2 = []
        self.G3 = []
        self.G4 = []
        self.GA = []
        self.GQ = []
        connection = sqlite3.connect("DataBase.db")
        cur = connection.cursor()
        sqlquery1 = "SELECT G1 FROM Quiz"
        sqlquery2 = "SELECT G2 FROM Quiz"
        sqlquery3 = "SELECT G3 FROM Quiz"
        sqlquery4 = "SELECT G4 FROM Quiz"
        sqlqueryQuestions = "SELECT questions FROM Quiz"
        sqlqueryA = "SELECT answer FROM Quiz"
        for row in cur.execute(sqlquery1):
            self.G1.append(row[0])
        for row in cur.execute(sqlquery2):
            self.G2.append(row[0])
        for row in cur.execute(sqlquery3):
            self.G3.append(row[0])
        for row in cur.execute(sqlquery4):
            self.G4.append(row[0])
        for row in cur.execute(sqlqueryQuestions):
            self.GQ.append(row[0])
        for row in cur.execute(sqlqueryA):
            self.GA.append(row[0])
        self.pushButton4.clicked.connect(lambda : self.WhichButtonPressed(1))
        self.pushButton5.clicked.connect(lambda : self.WhichButtonPressed(2))
        self.pushButton6.clicked.connect(lambda : self.WhichButtonPressed(3))
        self.pushButton7.clicked.connect(lambda : self.WhichButtonPressed(4))
        self.pushButton8.clicked.connect(self.GoResult)
        self.pushButton8.clicked.connect(self.FinalScore)

        self.IdArray = []
        co = sqlite3.connect("DataBase.db")
        cur = co.cursor()
        sqlquArr = "SELECT * FROM Info LIMIT 100000"
        for row in cur.execute(sqlquArr):
            self.IdArray.append(row[0])
        print(self.IdArray)
        self.IDUser = len(self.IdArray)+1
        print("IDUser is : ", self.IDUser)

        ###
        i = 0
        self.pushButton8.clicked.connect(lambda i=i: self.GoResult(self.score[i]))
        i += 1
        ###

    # def GoResult(self):
    #     widget.setCurrentIndex(2)
    #     widget.setFixedWidth(679)
    #     widget.setFixedHeight(246)

    def GoResult(self, id):
        ###
        QuizTest.who = id
        QuizTest.refresh()
        print(id)
        ###
        widget.setCurrentIndex(2)
        widget.setFixedWidth(679)
        widget.setFixedHeight(246)

    def GoNext(self):
        self.currentPic += 1
        self.currentPic = self.currentPic % (len(self.PhotoArray))
        self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
        self.pushButton4.setText(self.G1[self.currentPic])
        self.pushButton5.setText(self.G2[self.currentPic])
        self.pushButton6.setText(self.G3[self.currentPic])
        self.pushButton7.setText(self.G4[self.currentPic])

    def FinalScore(self):
        # NewScore = self.label2.text()
        # print(NewScore)
        LD = sqlite3.connect("DataBase.db")
        sqlLD = "UPDATE Info SET Score=" + str(self.score) + " WHERE ID=" + str(self.IDUser)
        LD.execute(sqlLD)
        LD.commit()
        LD.close()

    def WhichButtonPressed(self, Option):
        if len(self.PhotoArray) == 2:
            self.label3.setText("You passed the exam successfully! Congrats!")
            self.pushButton4.setText("You")
            self.pushButton5.setText("Did")
            self.pushButton6.setText("Your")
            self.pushButton7.setText("Best")


        elif Option == 1:
            if self.G1[self.currentPic] == self.GA[self.currentPic]:
                self.label3.setText("CORRECT")
                print("Success!")
                self.score += 1
                self.label2.setText(str(self.score))
                print(self.score)
                if self.currentPic != 0:
                    # eliminate This question:
                    self.PhotoArray.pop(self.currentPic)
                    self.G1.pop(self.currentPic)
                    self.G2.pop(self.currentPic)
                    self.G3.pop(self.currentPic)
                    self.G4.pop(self.currentPic)
                    self.GA.pop(self.currentPic)
                    self.GQ.pop(self.currentPic)
                    # go to Next Available Question:
                    self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
                    self.pushButton4.setText(self.G1[self.currentPic])
                    self.pushButton5.setText(self.G2[self.currentPic])
                    self.pushButton6.setText(self.G3[self.currentPic])
                    self.pushButton7.setText(self.G4[self.currentPic])

            else:
                print("Wrong answer")
                self.label3.setText("Wrong Answer")

        elif Option == 2:
            if self.G2[self.currentPic] == self.GA[self.currentPic]:
                self.label3.setText("CORRECT")
                print("Success!")
                self.score += 1
                self.label2.setText(str(self.score))
                print(self.score)
                if self.currentPic != 0:
                    # eliminate This question:
                    self.PhotoArray.pop(self.currentPic)
                    self.G1.pop(self.currentPic)
                    self.G2.pop(self.currentPic)
                    self.G3.pop(self.currentPic)
                    self.G4.pop(self.currentPic)
                    self.GA.pop(self.currentPic)
                    self.GQ.pop(self.currentPic)
                    # go to Next Available Question:
                    self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
                    self.pushButton4.setText(self.G1[self.currentPic])
                    self.pushButton5.setText(self.G2[self.currentPic])
                    self.pushButton6.setText(self.G3[self.currentPic])
                    self.pushButton7.setText(self.G4[self.currentPic])

            else:
                print("Wrong answer")
                self.label3.setText("Wrong Answer")

        elif Option == 3:
            if self.G3[self.currentPic] == self.GA[self.currentPic]:
                self.label3.setText("CORRECT")
                print("Success!")
                self.score += 1
                self.label2.setText(str(self.score))
                print(self.score)
                if self.currentPic != 0:
                    # eliminate This question:
                    self.PhotoArray.pop(self.currentPic)
                    self.G1.pop(self.currentPic)
                    self.G2.pop(self.currentPic)
                    self.G3.pop(self.currentPic)
                    self.G4.pop(self.currentPic)
                    self.GA.pop(self.currentPic)
                    self.GQ.pop(self.currentPic)
                    # go to Next Available Question:
                    self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
                    self.pushButton4.setText(self.G1[self.currentPic])
                    self.pushButton5.setText(self.G2[self.currentPic])
                    self.pushButton6.setText(self.G3[self.currentPic])
                    self.pushButton7.setText(self.G4[self.currentPic])

            else:
                print("Wrong answer")
                self.label3.setText("Wrong Answer")

        elif Option == 4:
            if self.G4[self.currentPic] == self.GA[self.currentPic]:
                self.label3.setText("CORRECT")
                print("Success!")
                self.score += 1
                self.label2.setText(str(self.score))
                print(self.score)
                if self.currentPic != 0:
                    # eliminate This question:
                    self.PhotoArray.pop(self.currentPic)
                    self.G1.pop(self.currentPic)
                    self.G2.pop(self.currentPic)
                    self.G3.pop(self.currentPic)
                    self.G4.pop(self.currentPic)
                    self.GA.pop(self.currentPic)
                    self.GQ.pop(self.currentPic)
                    # go to Next Available Question:
                    self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
                    self.pushButton4.setText(self.G1[self.currentPic])
                    self.pushButton5.setText(self.G2[self.currentPic])
                    self.pushButton6.setText(self.G3[self.currentPic])
                    self.pushButton7.setText(self.G4[self.currentPic])

            else:
                print("Wrong answer")
                self.label3.setText("Wrong Answer")

    def GoPrevious(self):
        self.currentPic -= 1
        self.currentPic = self.currentPic % (len(self.PhotoArray))
        self.PICS.setPixmap(QtGui.QPixmap(self.PhotoArray[self.currentPic]))
        self.pushButton4.setText(self.G1[self.currentPic])
        self.pushButton5.setText(self.G2[self.currentPic])
        self.pushButton6.setText(self.G3[self.currentPic])
        self.pushButton7.setText(self.G4[self.currentPic])

class Result(QDialog):
    # def __init__(self):
    ###
    def __init__(self, msg):
        ###
        super(Result, self).__init__()
        loadUi("Result.ui", self)
        self.pushButton.clicked.connect(self.New)
        ###
        self.who = msg
        self.refresh()
        ###

    ###
    def refresh(self):
        got = sqlite3.connect("DataBase.db")
        sabt = got.cursor()
        getData = "SELECT * FROM Info WHERE ID=" + str(self.who)
        for row in sabt.execute(getData):
            self.label2.setText(str(row[0]))
    ###

    def New(self):
        widget.setCurrentIndex(0)
        widget.setFixedWidth(755)
        widget.setFixedHeight(578)

app = QApplication(sys.argv)
InfoTest = Info()
QuizTest = Quiz()
###
ResultTest = Result(1)
###
# ResultTest = Result()
widget = QtWidgets.QStackedWidget()
widget.addWidget(InfoTest)
widget.addWidget(QuizTest)
widget.addWidget(ResultTest)
widget.setFixedWidth(755)
widget.setFixedHeight(578)
widget.show()
app.exit(app.exec_())

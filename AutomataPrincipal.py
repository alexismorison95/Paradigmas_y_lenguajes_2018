# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 18:25:42 2018

@author: Alexis
"""

import sys, time
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import QPixmap

from ayuda import Ayuda


menu = uic.loadUiType("interfaz/main2.ui")[0] 

class Ventana(QtGui.QMainWindow,menu):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self) 
        self.setWindowTitle("AFD mínimo")
        self.setWindowIcon(QtGui.QIcon(QPixmap("logoapp.png")))
        self.setFixedSize(self.size())
        
        self.imagen.setPixmap(QPixmap("AFD minimo.png"))
        
        self.play.setIcon(QtGui.QIcon(QPixmap('play.png')))
        
        self.stop.setIcon(QtGui.QIcon('Stop1NormalBlue_26947.ico'))
        
        self.validar.setIcon(QtGui.QIcon('check_ok_accept_apply_1582.ico'))
        
        self.limpiar.setIcon(QtGui.QIcon('delete_delete_exit_1577.ico'))
        
        self.label.setText("")
        
        self.limpiar.setFocus()
        
        self.play.setEnabled(False)
        
        self.stop.setEnabled(False)
                
        self.limpiar.clicked.connect(self.limpiarLine)
        
        self.validar.clicked.connect(self.funcion)
        
        self.play.clicked.connect(self.pasos)
        
        self.stop.clicked.connect(self.parar)
        
        self.opciones()
        
        self.andar = False
        
        self.lineEdit.textChanged.connect(self.proteccion)
        
        self.permitido = ["a","b"]
        
        self.func = {(1, 'a'):2,  (1, 'b'):3,
                     (2, 'a'):4,  (2, 'b'):5,
                     (3, 'a'):4,  (3, 'b'):6,
                     (4, 'a'):7,  (4, 'b'):8,
                     (5, 'a'):10, (5, 'b'):3,
                     (6, 'a'):7,  (6, 'b'):3,
                     (7, 'a'):4,  (7, 'b'):5,
                     (8, 'a'):9,  (8, 'b'):6,
                     (9, 'a'):10, (9, 'b'):10,
                     (10,'a'):9,  (10,'b'):9
                    }
                    
        self.finales = [10]
    
    

    def opciones(self):          
        self.statusBar()
        mainMenu = self.menuBar() 
        menu = QtGui.QAction("Léeme", self)
        menu.triggered.connect(self.metodo)
        fileMenu = mainMenu.addMenu('&Ayuda')
        fileMenu.addAction(menu)        

    
    def metodo(self):
        dial = Ayuda()
        dial.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dial.setWindowFlags(QtCore.Qt.Popup) 
        dial.setModal(True) 
        dial.exec_()
        QtGui.qApp.processEvents()
        self.lineEdit.setSelection(0,len(self.lineEdit.text()))
    
               
    def limpiarLine(self):
        self.lineEdit.clear()
        self.label.setText("")
        self.play.setEnabled(False)
        self.stop.setEnabled(False)
        self.limpiar.setEnabled(False)
        self.andar = False
        self.imagen.setPixmap(QPixmap("AFD minimo.png"))
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setCursorPosition(len(self.lineEdit.text()))
        
    
    def proteccion(self):
        self.andar = False
        self.label.setText("")
        self.validar.setEnabled(True)
        self.play.setEnabled(False)
        self.stop.setEnabled(False)
        self.imagen.setPixmap(QPixmap("AFD minimo.png"))       
        if(self.lineEdit.text() != ""):
            if(self.lineEdit.text()[len(self.lineEdit.text())-1].lower() not in self.permitido):
                aux = self.lineEdit.text()[0:len(self.lineEdit.text())-1]
                self.lineEdit.clear()
                self.lineEdit.setText(aux)
                
                
    def parar(self):
        self.andar = False
        self.imagen.setPixmap(QPixmap("AFD minimo.png"))
        self.limpiar.setEnabled(True)
        self.stop.setEnabled(False)
        self.play.setEnabled(True)
        self.lineEdit.setSelection(0,0)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setCursorPosition(len(self.lineEdit.text()))
        
        
    def pasos(self):
        self.andar = True
        self.validar.setEnabled(False)
        self.limpiar.setEnabled(False)
        self.play.setEnabled(False)
        self.stop.setEnabled(True)
        self.imagen.setPixmap(QPixmap("1.png"))
        self.lineEdit.setSelection(0,0)
        self.lineEdit.setReadOnly(True)
        start = time.time()
        while(time.time() - start < 2): 
            QtGui.qApp.processEvents()
        self.automataPasos(self.lineEdit.text().lower(),1,self.func,self.finales,1)
        self.andar = False
        self.limpiar.setEnabled(True)
        self.play.setEnabled(True)
        self.stop.setEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setCursorPosition(len(self.lineEdit.text()))
        
                
    def automataPasos(self, cadena, estadoActual, funcion, finales, cont):  
        if((cadena != "") and (self.andar)):
            self.lineEdit.setSelection(0,cont)
            self.imagen.setPixmap(QPixmap(str(estadoActual)+" "+str(funcion[(estadoActual, cadena[0])])+" "+cadena[0]+".png"))                 
            start = time.time()
            while((time.time() - start < 2) and (self.andar)):
                QtGui.qApp.processEvents()  
            self.automataPasos(cadena[1:], funcion[(estadoActual, cadena[0])], funcion, finales, cont+1)
                            
    
    def automata(self, cadena, estadoActual, funcion, finales):    
        if(cadena == ""):                     
            return estadoActual in finales      
        else: 
            return self.automata(cadena[1:], funcion[(estadoActual, cadena[0])], funcion, finales)
    
    
    def funcion(self):
        self.play.setEnabled(True)
        self.stop.setEnabled(False)
        self.validar.setEnabled(False)
        self.limpiar.setEnabled(True)
        self.andar = False
        self.imagen.setPixmap(QPixmap("AFD minimo.png"))   
        if(self.automata(self.lineEdit.text().lower(),1 ,self.func ,self.finales)):
            self.label.setText("CADENA VÁLIDA")
            self.label.setStyleSheet('color: green; font: 16pt "MS Shell Dlg 2";')
        else:
            self.label.setText("CADENA NO VÁLIDA")
            self.label.setStyleSheet('color: red; font: 16pt "MS Shell Dlg 2";')
        
    
   
app = QtGui.QApplication(sys.argv)
principal = Ventana()
principal.show()
app.exec_()
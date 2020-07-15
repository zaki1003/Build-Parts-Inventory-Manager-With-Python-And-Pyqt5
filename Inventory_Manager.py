# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication


import sys,os

from os import path

def resource_path(relative_path):
      if hasattr(sys, '_MEIPASS'):
           return os.path.join(sys._MEIPASS, relative_path)
      return os.path.join(os.path.abspath("."), relative_path)



from PyQt5.uic import loadUiType

FORM_CLASS,_=loadUiType(resource_path("main.ui"))

import sqlite3



x=0
idx=0

class Main(QMainWindow, FORM_CLASS):
    # Constructeur 
    def __init__(self,parent=None):
          super(Main,self).__init__(parent)
          QMainWindow.__init__(self)
          self.setupUi(self)
          self.Handel_Buttons()   #Pour Manupiler les cliques dans notre buttons
        
          
          
    # function 
    def Handel_Buttons(self):
        #Here is our code
       self.refresh_btn.clicked.connect(self.GET_DATA) 
       self.search_btn.clicked.connect(self.SEARCH) 
       self.check_btn.clicked.connect(self.LEVEL) 
       self.update_btn.clicked.connect(self.UPDATE) 
       self.delete_btn.clicked.connect(self.DELETE)
       self.add_btn.clicked.connect(self.ADD)
       self.next_btn.clicked.connect(self.NEXT)
       self.previous_btn.clicked.connect(self.PREVIOUS)
       self.last_btn.clicked.connect(self.LAST)
       self.first_btn.clicked.connect(self.FIRST)
       
       
       
       
       
    
    
    def GET_DATA(self):        
        #Connect to Sqlite3 database and fill GUI table with data.
        db=sqlite3.connect(resource_path("parts.db"))
        cursor=db.cursor()
        command=''' SELECT * from parts_table  '''
        
        result=cursor.execute(command)
        
        self.table.setRowCount(0)     #initialiser le nbr des lignes detableau 
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
     
        
        
        #Display references number and type number in statistics tab
        cursor2=db.cursor()
        cursor3=db.cursor()
        
        parts_nbr=''' SELECT COUNT (DISTINCT PartName) FROM parts_table ''' # COUNT :calculer le nombre des differnets partName
        ref_nbr= ''' SELECT COUNT (DISTINCT Reference) FROM parts_table ''' # COUNT :calculer le nombre des differnets Reference
        
        result_ref_nbr=cursor2.execute(ref_nbr) # executer la fonction ref_nbr et mettre le resultat dans result_ref_nbr
        result_parts_nbr=cursor3.execute(parts_nbr)
        
        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0])) #fetchone()[0] pour prendre la premiére ligne
        self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))
        
        # Display 4 results: Min,Max Nbr of holes in addition to their respective reference names
        
        cursor4=db.cursor()
        cursor5=db.cursor()
        
        min_hole=''' SELECT MIN(NumberOfHoles), Reference from parts_table '''
        max_hole=''' SELECT MAX(NumberOfHoles), Reference from parts_table '''
        
        result_min_hole=cursor4.execute(min_hole)
        result_max_hole=cursor5.execute(max_hole)
        
        r1=result_min_hole.fetchone() #fetchone pour selectioner 1ere ligne,l'instruction complet ta3tina ki tablaua kima hak [min_hole:5, reference:WF456]     sama r1[0] homa nbr of holes w r1[1] howa lifih reference
        r2=result_max_hole.fetchone()
        
        # Print Reslt in QLabels
        
        self.lbl_min_hole.setText(str(r1[0]))
        self.lbl_max_hole.setText(str(r2[0]))
        
        self.lbl_min_hole_2.setText(str(r1[1]))
        self.lbl_max_hole_2.setText(str(r2[1]))
        
        
        self.FIRST()
        self.NAVIGATE()
        
        
        
        
        
        
    def SEARCH(self):
          
          db=sqlite3.connect(resource_path("parts.db"))
          cursor=db.cursor()
          nbr=int(self.count_filter_txt.text())
          command=''' SELECT * from parts_table WHERE count<=? '''
         #Dans command on a utiliser '?' pour passer la valeur de nbr Dans l'execution du curseur on ecrivons   command,[nbr]
          result=cursor.execute(command, [nbr])
    
          self.table.setRowCount(0)     #initialiser le nbr des lignes detableau 
        
          for row_number, row_data in enumerate(result):
              self.table.insertRow(row_number)
              for column_number, data in enumerate(row_data):
                  self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))  #remplire le tableau 'table'
    
    
    def LEVEL(self):
        db=sqlite3.connect(resource_path("parts.db"))
        cursor=db.cursor()
        command=''' SELECT Reference, PartName, Count from parts_table ORDER BY Count asc LIMIT 3  '''
        
        result=cursor.execute(command)
        
        self.table2.setRowCount(0)     #initialiser le nbr des lignes detableau 
        
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
     
    
    
    def NAVIGATE(self):
       global idx 
       db=sqlite3.connect(resource_path("parts.db"))
       cursor=db.cursor()
    
       command=''' SELECT * from parts_table WHERE ID=? '''
       
       result=cursor.execute(command,[idx])
       Val=result.fetchone()
    
       self.id.setText(str(Val[0]))
       self.reference.setText(str(Val[1]))
       self.part_name.setText(str(Val[2]))
       self.min_area.setText(str(Val[3]))
       self.max_area.setText(str(Val[4]))
       self.number_of_holes.setText(str(Val[5]))
       self.min_diameter.setText(str(Val[6]))
       self.max_diameter.setText(str(Val[7]))
       self.count.setValue(Val[8])
       
    def NEXT(self):
           db=sqlite3.connect(resource_path("parts.db"))
           cursor=db.cursor()
       
           command=''' SELECT ID FROM parts_table '''
           result=cursor.execute(command)
           val=result.fetchall()
           tot=len(val)
           global x
           global idx
           x=x+1
           if x<tot : 
               idx=val[x][0]
               self.NAVIGATE()
           else:
               x=tot-1
               print("End of file")   #les instructions print à la fin ne sont que pour le débogage, vous pouvez les supprimer si vous le souhaitez)
    
  


    def PREVIOUS(self):
           db=sqlite3.connect(resource_path("parts.db"))
           cursor=db.cursor()
       
           command=''' SELECT ID FROM parts_table '''
           result=cursor.execute(command)
           val=result.fetchall()
           tot=len(val)
           global x
           global idx
           x=x-1
           if x>-1:
               idx=val[x][0]
               self.NAVIGATE()
           else:
               x=0
               print("Begin of file")
               


    def LAST(self):
           db=sqlite3.connect(resource_path("parts.db"))
           cursor=db.cursor()
       
           command=''' SELECT ID FROM parts_table '''
           result=cursor.execute(command)
           val=result.fetchall()
           tot=len(val)
           global x
           global idx
           x=tot-1 
           if x<tot:
               idx=val[x][0]
               self.NAVIGATE()
           else:
               x=tot-1
               print("End of file")
               
               
               
               
               
               
               
               
               
    def FIRST(self):
           db=sqlite3.connect(resource_path("parts.db"))
           cursor=db.cursor()
       
           command=''' SELECT ID FROM parts_table '''
           result=cursor.execute(command)
           val=result.fetchall()
    
           global x
           global idx
           
           x=0
           if x>-1:
               idx=val[x][0]
               self.NAVIGATE()
           else:
               x=0
               print("Begin of file")





               
               
    
    def UPDATE(self):
        db=sqlite3.connect(resource_path("parts.db"))
        cursor=db.cursor()  
        
        
        id_=int(self.id.text()) # tous ce qu'est dans la zone de texte id il sera stocker dans la variable id
        refernce_=self.reference.text() # tous ce qu'est dans la zone de texte reference il sera stocker dans la variable reference
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        number_of_holes_=self.number_of_holes.text()
        min_diameter_=self.min_diameter.text()
        max_diameter_=self.max_diameter.text()
        count_=str(self.count.value())
        
        
        row=(refernce_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_,id_)
        
        
        command=''' UPDATE parts_table SET Reference=?,PartName=?,MinArea=?,MaxArea=?,NumberOfHoles=?,MinDiameter=?,MaxDiameter=?,Count=? WHERE ID=? '''
        #Dans command on a utiliser '?' pour passer le tableau row (howa ghi ligne wa7da ) Dans l'execution du curseur on ecrivons   command,row 
        
        cursor.execute(command,row)
        
        db.commit()
        
        
       
    def DELETE(self):
        db=sqlite3.connect(resource_path("parts.db"))
        cursor=db.cursor()
        
        d=self.id.text()
         
        command=''' DELETE FROM parts_table WHERE ID=? '''
        
        cursor.execute(command,d)
        
        db.commit()
        
        
    def ADD(self):
    
        db=sqlite3.connect(resource_path("parts.db"))
        cursor=db.cursor()  
        
        
        refernce_=self.reference.text() # tous ce qu'est dans la zone de texte reference il sera stocker dans la variable reference
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        number_of_holes_=self.number_of_holes.text()
        min_diameter_=self.min_diameter.text()
        max_diameter_=self.max_diameter.text()
        count_=str(self.count.value())
        
        
        row=(refernce_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_)
        
        
        command=''' INSERT INTO parts_table ( Reference,PartName,MinArea,MaxArea,NumberOfHoles,MinDiameter,MaxDiameter,Count) VALUES(?,?,?,?,?,?,?,?) '''
        #Dans command on a utiliser '?' pour passer le tableau row (howa ghi ligne wa7da ) Dans l'execution du curseur on ecrivons   command,row 
        
        cursor.execute(command,row)
        
        db.commit()
             
        
        
       
        
        
        
        
        
        
    
    
def main():    #khass ykono las9in m3a l7ayt
     app=QApplication(sys.argv)
     window=Main()
     window.show()
     app.exec_()
     
     
if __name__=='__main__':    #khass ykono las9in m3a l7ayt
      main()
          
          

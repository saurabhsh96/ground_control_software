#GCS GUI Version 1.0
#This is the central module of the GCS.(tick)
#It imports functions and storage modules.(tick)
#As soon as the GCS is started an infinite instance for checking the input(tick)
#is turned on so that the storage module will check input(tick)
#constantly and store if required.(tick)
#All of them meet here, signals calls the respective function and the
#work is done by that function. (tick)

'''NOTES:
Define signals to be sent to detach, as fsw_signal and as telemetry swich
GPS DATA too can be simulteneously updated'''

import sys
import sqlite3
from threading import Thread 
import time
sys.path.insert(1, '/home/saurabh/Desktop/GCS/')

import storage3 #module which recieves and stores the data. 
try:
    from gi.repository import Gtk, Gdk #importing Gtk+3
except:
    print("Gtk Not Found!") 
    sys.exit(1) #exit if not found
import functions
#import functions #module containing the functions
import plot
x=[] #list which will contain the last row details
'''from_value = 0
to_value = 100
Needed for later purposes'''
    
class GUI(functions.functions): #class functions from module functions
                                #is inherited in this class
    wTree = None #Widget Tree
    
    def __init__(self):
        self.wTree = Gtk.Builder() #Gtk wTree, builds the widget tree
        self.wTree.add_from_file("/home/saurabh/Desktop/GCS/gui.glade")
        
        self.dic = dict(
            #mainwindow signals
            on_main_w_destroy = self.quit,
            on_show_def_clicked = self.show_def,
            on_hide_def_clicked = self.hide_def,
            on_hide_all_clicked = self.hide_all,
            on_graph_s_toggled = self.graph_settings,
            on_gps_data_toggled = self.gps_data,
            on_tel_switch_activate = self.telemeter,
            on_alt_toggled = self.altitude,
            on_in_temp_toggled = self.in_temp,
            on_out_temp_toggled = self.out_temp,
            on_pressure_toggled = self.pressure,
            on_voltage_toggled = self.voltage,
            on_bonus_toggled = self.bonus,
            on_detach_clicked = self.detach,
            #Graph window signals
            on_graph_settings_delete_event = self.graph_s_quit,
            on_alt_g_toggled = self.alt_graph,
            on_int_g_toggled = self.in_t_graph,
            on_outt_g_toggled = self.out_t_graph,
            on_pressure_g_toggled = self.pressure_graph,
            on_voltage_g_toggled = self.voltage_graph,
            on_bonus_g_toggled = self.bonus_graph,
            on_time_g_toggled = self.time_graph,
            on_cust_plot_clicked = self.cust_plot,
            on_reset_clicked = self.reset,
            on_window1_destroy = self.window1_quit,
            on_enter_clicked = self.enter,
            )

        self.wTree.connect_signals(self.dic)
        self.wTree.get_object("time_g").set_active(True)
        self.wTree.get_object("tel_switch").set_active(True)
          
    def last_received(self):
        db = sqlite3.connect('/home/saurabh/Desktop/GCS/storage.db')
        c = db.cursor()
        while(1):
            time.sleep(0.001)
            c.execute("SELECT * FROM telemetry WHERE ROWID= (SELECT max(ROWID) FROM telemetry)")
            x=c.fetchone()
            db.commit()
            #print x
            Gdk.threads_enter() 
            self.wTree.get_object("entry1").set_text(str(x[1]))
            self.wTree.get_object("entry2").set_text(str(x[6]))
            self.wTree.get_object("entry3").set_text(str(x[2]))
            self.wTree.get_object("entry4").set_text(str(x[3]))
            self.wTree.get_object("entry5").set_text(str(x[4]))
            self.wTree.get_object("entry6").set_text(str(x[7]))
            self.wTree.get_object("entry7").set_text(str(x[5]))
            self.wTree.get_object("entry8").set_text(str(x[8]))
            self.wTree.get_object("entry9").set_text(str(x[13]))
            Gdk.threads_leave()
        db.close()     
                
def func1():
    while True:
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()
        
def func2():
    while True:
        storage3.main()

if __name__=="__main__":
    generate = GUI()
    Gdk.threads_init()
    t1=Thread(target = func2)
    t2=Thread(target = func1)
    t3=Thread(target = generate.last_received)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t1.start()
    t2.start()
    t3.start()
    while True:
        pass
               
               
               
        
            
            
            

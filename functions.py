#GCS functions version 1.0
#imports the plot module and is imported in the GUI module
#contains all the functions for each of the signal
#passes the parameters to the plot module

class mpl:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
    from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

import sys
import time
sys.path.insert(1, '/home/saurabh/Desktop/GCS/')
import storage3
from threading import Thread
try:
    from gi.repository import Gtk, Gdk, GLib, GObject
except:
    print("Gtk Not Found!")
    sys.exit(1)
Gdk.threads_init()
import plot
entry_f = "NULL"
entry_t = "NULL"
entry_y = "NULL"
entry_w = "NULL"

first_para = ""
g1 = None
g2 = None
g3 = None
g4 = None
g5 = None
g6 = None

class functions():
                              
    def show_def(self, object):
        
        if (self.wTree.get_object("in_temp").get_active()==True or
            self.wTree.get_object("out_temp").get_active()==True or
            self.wTree.get_object("pressure").get_active()==True or
            self.wTree.get_object("voltage").get_active()==True):
            self.wTree.get_object("in_temp").set_active(False)
            self.wTree.get_object("out_temp").set_active(False)
            self.wTree.get_object("pressure").set_active(False)
            self.wTree.get_object("voltage").set_active(False)
        
        if (self.wTree.get_object("alt").get_active()==False or
            self.wTree.get_object("bonus").get_active()==False):
            self.wTree.get_object("alt").set_active(True)
            self.wTree.get_object("bonus").set_active(True)
            
        else:
            print "Default graphs are already active!"

    def hide_def(self, object):
        if (self.wTree.get_object("alt").get_active()==True or
            self.wTree.get_object("bonus").get_active()==True):
            self.wTree.get_object("alt").set_active(False)
            self.wTree.get_object("bonus").set_active(False)
        else:
            print "Default graphs are already inactive!"

    def hide_all(self, object):
        if(self.wTree.get_object("alt").get_active()==True):
            self.wTree.get_object("alt").set_active(False)
        elif(self.wTree.get_object("in_temp").get_active()==True):
            self.wTree.get_object("in_temp").set_active(False)
        elif(self.wTree.get_object("out_temp").get_active()==True):
            self.wTree.get_object("out_temp").set_active(False)
        elif(self.wTree.get_object("pressure").get_active()==True):
            self.wTree.get_object("pressure").set_active(False)
        elif(self.wTree.get_object("voltage").get_active()==True):
            self.wTree.get_object("voltage").set_active(False)
        elif(self.wTree.get_object("bonus").get_active()==True):
            self.wTree.get_object("bonus").set_active(False)
        else:
            print("No active graphs found!")
            
    def graph_settings(self, object):
        if (self.wTree.get_object("graph_s").get_active()==True):
            self.wTree.get_object("graph_settings").show_all()
        else:
            self.wTree.get_object("graph_settings").hide()
    
    def gps_data(self, object):
        if(self.wTree.get_object("gps_data").get_active()==True):
            with open ("/home/saurabh/Desktop/GCS/gps_data") as f:
                for row in f:
                    print row
            self.wTree.get_object("gps_data").set_active(False)
        else:
            pass
        
    def telemeter(self, object):
        if(self.wTree.get_object("tel_switch").get_active()==True):
            storage3.telemetry_start()
        else:
            storage3.telemetry_stop()

    def detach(self, object):
        #send some signal to detach the module
        self.wTree.get_object("detach").set_sensitive(False)
        storage3.detach()
        
    def quit(self, object):
        sys.exit(0)
    #graph window functions checkbutton function

    def alt_graph(self, object):
        global first_para
        if(self.wTree.get_object("alt_g").get_active()==True):
            first_para="ALT_SENSOR"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
                    
    def in_t_graph(self, object):
        global first_para
        if(self.wTree.get_object("int_g").get_active()==True):
            first_para="INSIDE_TEMP"
            self.wTree.get_object("alt_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
        
    def out_t_graph(self, object):
        global first_para
        if(self.wTree.get_object("outt_g").get_active()==True):
            first_para="OUTSIDE_TEMP"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("alt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
            
    def pressure_graph(self, object):
        global first_para
        if(self.wTree.get_object("pressure_g").get_active()==True):
            first_para="PRESSURE"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("alt_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
        
    def voltage_graph(self, object):
        global first_para
        if(self.wTree.get_object("voltage_g").get_active()==True):
            first_para="VOLTAGE"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("alt_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
    
    def bonus_graph(self, object):
        global first_para    
        if(self.wTree.get_object("bonus_g").get_active()==True):
            first_para="ROTOR_RATE"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("alt_g").set_active(False)
            self.wTree.get_object("time_g").set_active(False)
        
    def time_graph(self, object):
        global first_para
        if(self.wTree.get_object("time_g").get_active()== True):
            first_para="MISSION_TIME"
            self.wTree.get_object("int_g").set_active(False)
            self.wTree.get_object("outt_g").set_active(False)
            self.wTree.get_object("pressure_g").set_active(False)
            self.wTree.get_object("voltage_g").set_active(False)
            self.wTree.get_object("bonus_g").set_active(False)
            self.wTree.get_object("alt_g").set_active(False)

    def enter(self, object):

        global entry_f
        global entry_t
        global entry_y
        global entry_w

        entry_f = self.wTree.get_object("entry11").get_text()
        entry_t = self.wTree.get_object("entry12").get_text()
        entry_w = self.wTree.get_object("entry9").get_text()
        entry_y = self.wTree.get_object("entry10").get_text()
        
    def cust_plot(self, object):

        global entry_f
        global entry_t
        global entry_y
        global entry_w
        
        if((int(entry_f)>=0)&(int(entry_t)<=int(entry_w))&(int(entry_f)!=int(entry_t))):
            #mpl
            figure = mpl.Figure(figsize=(5,5), dpi=100)
            ax = figure.add_subplot(1, 1, 1)
            ax.grid(True)
            canvas = mpl.FigureCanvas(figure)
            toolbar = mpl.NavigationToolbar(canvas, self.wTree.get_object("window1"))
            ax.set_xlabel(first_para)
            #data
            f= open('/home/saurabh/Desktop/GCS/normal', 'r').read()
            x = f.split('\n')
            y=''
            i = int(entry_f)
            char=''
            z = []
            fp=[]
            sp=[]
            row = ''
            while(i<=int(entry_t)):
                row = x[i]
                if (len(row)>1):
                    for j in range(len(row)):
                        char = row[j]
                        if(char == ','):
                            z.append(y)
                            y =''
                            continue
                        if(j==len(row)-1):
                            z.append(char)
                            continue
                        y = y + char
                        j += 1
                    if (first_para=="MISSION_TIME"):
                        fp.append(int(z[1]))
                    elif (first_para=="ALT_SENSOR"):
                        fp.append(float(z[2]))
                    elif (first_para=="INSIDE_TEMP"):
                        fp.append(float(z[4]))
                    elif (first_para=="OUTSIDE_TEMP"):
                        fp.append(float(z[3]))
                    elif (first_para=="VOLTAGE"):
                        fp.append(float(z[5]))
                    elif (first_para=="PRESSURE"):
                        fp.append(float(z[7]))
                    else:
                        fp.append(float(z[8]))
                    if (entry_y=="ALTITUDE"):
                        sp.append(float(z[2]))
                    elif (entry_y=="INSIDE_TEMP"):
                        sp.append(float(z[4]))
                    elif (entry_y=="OUTSIDE_TEMP"):
                        sp.append(float(z[3]))
                    elif (entry_y=="VOLTAGE"):
                        sp.append(float(z[5]))
                    elif (entry_y=="PRESSURE"):
                        sp.append(float(z[7]))
                    else:
                        sp.append(float(z[8]))
                    z[:]=[]
                i+=1
                  
            if (entry_y=="ALTITUDE"):
                ax.set_ylim(0, 500)
                ax.set_ylabel("Altitude")
                line, = ax.plot(fp, sp, color='blue')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()

            elif (entry_y=="INSIDE_TEMP"):
                ax.set_ylim(0, 30)
                ax.set_ylabel("Inside Temperature")
                self.line, = ax.plot(fp, sp, color='green')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()
                
            elif (entry_y=="OUTSIDE_TEMP"):
                ax.set_ylim(0, 50)
                ax.set_ylabel("Outside Temperature")
                self.line, = ax.plot(fp, sp, color='red')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()
                
            elif (entry_y=="VOLTAGE"):
                ax.set_ylim(0, 12)
                ax.set_ylabel("Voltage")
                self.line, = ax.plot(fp, sp, color='yellow')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()
                
            elif (entry_y=="PRESSURE"):
                ax.set_ylim(0, 500)
                ax.set_ylabel("Pressure")
                self.line, = ax.plot(fp, sp, color='black')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()
                
            else:
                ax.set_ylim(0, 5000)
                ax.set_ylabel("Rotor Rate")
                self.line, = ax.plot(fp, sp, color='violet')
                self.wTree.get_object("ssw1").add(canvas)
                self.wTree.get_object("ssw2").add(toolbar)
                self.wTree.get_object("window1").show_all()
        else:
            self.wTree.get_object("label40").set_text(
                "The values provided are invalid!"
                )

    def window1_quit(self, object):
        Gtk.main_quit()
        
    def reset(self, object):
       self.wTree.get_object("entry11").set_text("NULL")
       self.wTree.get_object("entry12").set_text("NULL")
       self.wTree.get_object("entry10").set_text("NULL")
                    
    #main window checkbutton functions
    def altitude(self, object):
        global g1
        if(self.wTree.get_object("alt").get_active()==True):
            g1 = plot.exe()
            g1.plot2(first_para, "ALTITUDE")
        else:
            g1.plot3()
        
    def in_temp(self, object):
        global g2
        if(self.wTree.get_object("in_temp").get_active()==True):
            g2 = plot.exe()
            g2.plot2(first_para, "INSIDE_TEMP")
        else:
            g2.plot3()
        
    def out_temp(self, object):
        global g3
        if(self.wTree.get_object("out_temp").get_active()==True):
            g3 = plot.exe()
            g3.plot2(first_para, "OUTSIDE_TEMP")
        else:
            g3.plot3()
        
    def voltage(self, object):
        global g4
        if(self.wTree.get_object("voltage").get_active()==True):
            g4 = plot.exe()
            g4.plot2(first_para, "VOLTAGE")
        else:
            g4.plot3()
        
    def pressure(self, object):
        global g5
        if(self.wTree.get_object("pressure").get_active()==True):
            g5 = plot.exe()
            g5.plot2(first_para, "PRESSURE")
        else:
            g5.plot3()
        
    def bonus(self, object):
        global g6
        if(self.wTree.get_object("bonus").get_active()==True):
            g6 = plot.exe()
            g6.plot2(first_para, "ROTOR_RATE")
        else:
            g6.plot3()
        
    def graph_s_quit(self, object, event=None):
        return True
        
if __name__=="__main__":
    generate = functions()
    

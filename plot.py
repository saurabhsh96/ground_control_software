from gi.repository import Gtk, Gdk
import time
from threading import Thread
from multiprocessing import Process
import sys

class mpl:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
    from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

class plot():

    def __init__(self, *args):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/saurabh/Desktop/GCS/plot_test.glade")
        dic = dict(
            on_window1_delete_event = self.delete_event,
            )
        self.builder.connect_signals(dic)
        #self.builder.get_object("window1").set_decorated(False)
        self.builder.get_object("window1").set_title(str(args[1]))
        #Data
        self.fp=[]
        self.sp=[]
        #MPL
        self.figure = mpl.Figure(figsize=(5,5), dpi=100)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.grid(True)
        self.canvas = mpl.FigureCanvas(self.figure)
        self.toolbar = mpl.NavigationToolbar(self.canvas, self.builder.get_object("window1"))
        self.ax.set_title(str(args[0])+" vs "+str(args[1]))
        
        if (args[0]=="MISSION_TIME"):
            self.ax.set_xlim(0, 300)
            self.ax.set_xlabel("Mission Time (seconds)")
        elif (args[0]=="ALT_SENSOR"):
            self.ax.set_xlim(0, 1000)
            self.ax.set_xlabel("Altitude (meters)")
        elif (args[0]=="INSIDE_TEMP"):
            self.ax.set_xlim(0, 100)
            self.ax.set_xlabel("Inside Temperature (celsius)")
        elif (args[0]=="OUTSIDE_TEMP"):
            self.ax.set_xlim(0, 100)
            self.ax.set_xlabel("Outside Temperature (celsius)")
        elif (args[0]=="VOLTAGE"):
            self.ax.set_xlim(0, 12)
            self.ax.set_xlabel("Voltage (volts)")
        elif (args[0]=="PRESSURE"):
            self.ax.set_xlim(0, 100000)
            self.ax.set_xlabel("Pressure (pascal)")
        else:
            self.ax.set_xlim(0, 5000)
            self.ax.set_xlabel("Rotor Rate (RPM)")

        if (args[1]=="ALTITUDE"):
            self.ax.set_ylim(0, 1000)
            self.ax.set_ylabel("Altitude (meters)")
            self.line, = self.ax.plot(self.fp, self.sp, color='blue')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()

        elif (args[1]=="INSIDE_TEMP"):
            self.ax.set_ylim(0, 100)
            self.ax.set_ylabel("Inside Temperature (celsius)")
            self.line, = self.ax.plot(self.fp, self.sp, color='green')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()
            
        elif (args[1]=="OUTSIDE_TEMP"):
            self.ax.set_ylim(0, 100)
            self.ax.set_ylabel("Outside Temperature (celsius)")
            self.line, = self.ax.plot(self.fp, self.sp, color='red')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()
            
        elif (args[1]=="VOLTAGE"):
            self.ax.set_ylim(0, 12)
            self.ax.set_ylabel("Voltage (volts)")
            self.line, = self.ax.plot(self.fp, self.sp, color='black')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()
            
        elif (args[1]=="PRESSURE"):
            self.ax.set_ylim(0, 100000)
            self.ax.set_ylabel("Pressure (pascal)")
            self.line, = self.ax.plot(self.fp, self.sp, color='yellow')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()
            
        else:
            self.ax.set_ylim(0, 5000)
            self.ax.set_ylabel("Rotor Rate (RPM)")
            self.line, = self.ax.plot(self.fp, self.sp, color='violet')
            self.builder.get_object("sw1").add(self.canvas)
            self.builder.get_object("sw2").add(self.toolbar)
            self.builder.get_object("window1").show_all()
        
    def data(self, *args):
        f= open('/home/saurabh/Desktop/GCS/normal', 'r').read()
        x = f.split('\n')
        y=''
        char=''
        z = []
        self.fp[:]=[]
        self.sp[:]=[]
        try:
            for row in x:
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
                    if (args[0]=="MISSION_TIME"):
                        self.fp.append(int(z[1]))
                    elif (args[0]=="ALT_SENSOR"):
                        self.fp.append(float(z[2]))
                    elif (args[0]=="INSIDE_TEMP"):
                        self.fp.append(float(z[4]))
                    elif (args[0]=="OUTSIDE_TEMP"):
                        self.fp.append(float(z[3]))
                    elif (args[0]=="VOLTAGE"):
                        self.fp.append(float(z[5]))
                    elif (args[0]=="PRESSURE"):
                        self.fp.append(float(z[7]))
                    else:
                        self.fp.append(float(z[8]))
                    if (args[1]=="ALTITUDE"):
                        self.sp.append(float(z[2]))
                    elif (args[1]=="INSIDE_TEMP"):
                        self.sp.append(float(z[4]))
                    elif (args[1]=="OUTSIDE_TEMP"):
                        self.sp.append(float(z[3]))
                    elif (args[1]=="VOLTAGE"):
                        self.sp.append(float(z[5]))
                    elif (args[1]=="PRESSURE"):
                        self.sp.append(float(z[7]))
                    else:
                        self.sp.append(float(z[8]))
                    z[:]=[]
            return self.fp, self.sp
        except:
            print(ValueError)
    def update(self, *args):
        x, y = self.data(args[0], args[1])
        self.line.set_xdata(x)
        self.line.set_ydata(y)
        self.ax.relim()
        self.ax.autoscale_view(False, False, True)
        self.canvas.draw()
        
    def run(self, *args):
        while True:
            while(1):
                Gdk.threads_enter()
                self.update(args[0], args[1])
                Gdk.threads_leave()

    def quit(self, object, event=None):
        Gtk.main_quit()
        return True

    def delete_event(self, object, event=None):
        return True
        
    def func(self):
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()
        
class exe():

    pl = None
        
    def plot2(self, *args):
        self.pl = plot(args[0], args[1])
        Gdk.threads_init()
        self.t1=Thread(target = self.pl.run, args = (args[0], args[1]))
        self.t2=Thread(target = self.pl.func)
        self.t1.start()
        self.t2.start()
    
    def plot3(self):
        self.pl.builder.get_object("window1").destroy()
        

#GCS storage veorsion 3.0
import serial
import csv
import time
import sqlite3
import sys
sys.path.insert(1, '/home/saurabh/Desktop/GCS/')

#Recieve serial data from the XBEE (tick)
#After every one second the program will check if there is an input? (tick)
#Separate each field in the data and store that under (tick)
#respective fields in DB named storage.db, telemetry is a table (tick)
#Separate the data and write a CSV file named (tick)
#telemetry.csv with a comma as a separator (tick) 
#storage module will be imported in functions and GUI and used there(tick);
ip = serial.Serial('/dev/ttyACM2', 9600, timeout=0, xonxoff=False, rtscts=False, dsrdtr=False)
sent = ('A', 'B', 'C', 'D', 'E')
flag = 0
def main():
    global flag;
    global ip;
    global sent;
    db = sqlite3.connect('/home/saurabh/Desktop/GCS/storage.db') #database created
    c = db.cursor() #c is the cursor in database file
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry(
                 TEAM_ID INTEGER, MISSION_TIME INTEGER, ALT_SENSOR REAL, OUTSIDE_TEMP REAL,
                 INSIDE_TEMP REAL, VOLTAGE REAL, FSW_STATE INTEGER, PRESSURE REAL,
                 ROTOR_RATE REAL, LATTITIDE REAL, LAT_CHAR TEXT, LONGITUDE REAL, LON_CHAR,
                 ROWID INTEGER PRIMARY KEY AUTOINCREMENT)'''); #Table created
    fp = open('/home/saurabh/Desktop/GCS/telemetry.csv', 'ab') #CSV file created or opened
    gps_data = open('/home/saurabh/Desktop/GCS/gps_data', 'a') #simple text file to store gps data, used by Gtk_button GPS_DATA
    #gps_data = open('/home/saurabh/Desktop/GCS/gps_data', 'w') #for an infinite loop 
    #fp = open('/home/saurabh/Desktop/GCS/telemetry.csv', 'wb') #CSV file created or opened for infinite loop    
    writer = csv.writer(fp, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow((
        'TEAM_ID', 'MISSION_TIME', 'ALT_SENSOR', 'OUTSIDE_TEMP',
        'INSIDE_TEMP', 'VOLTAGE', 'FSW_STATE', 'PRESSURE', 'ROTOR_RATE',
        'LATTITIDE', 'LAT_CHAR', 'LONGITUDE', 'LON_CHAR'))#writes the title row in csv file
    #fp.close()
    normal = open('/home/saurabh/Desktop/GCS/normal', 'a')
    #ip = serial.Serial('/dev/ttyACM0', 9600, timeout=0, xonxoff=False, rtscts=False, dsrdtr=False) #program set to recieve data   
    x = [] #taking care of lagged input also
    z =[]
    i                = 0 #mail looping variable, storing of recieved strings in list x
    j = 0 #for loop count to separate values in x
    y=''
    gps_string=''
    while(1): #infinite loop
        time.sleep(1)
        fp = open('/home/saurabh/Desktop/GCS/telemetry.csv', 'ab') #used for an infinite loop
        gps_data = open('/home/saurabh/Desktop/GCS/gps_data', 'a') #used for an infinite loop
        normal = open('/home/saurabh/Desktop/GCS/normal', 'a')
        x.append(ip.readline().rstrip())
        #print(x)
        ip.flushInput()
        for j in range(len(x[i])):
            char = x[i][j]
            if(char == ','):
                z.append(y)
                y =''
                continue
            if(j==len(x[i])-1):
                z.append(char)
                continue
            y = y + char
            j += 1
        try:
            c.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)", (
                int(z[0]), int(z[1]), float(z[2]), float(z[3]), float(z[4]), float(z[5]), int(z[6]), float(z[7]),
                float(z[8]), float(z[9]), str(z[10]), float(z[11]), str(z[12])));  #saved in the database named storage and table named telemetry
            db.commit()
            writer.writerow(z)
            #not needed we can append file is used instead or will be used in case of infinite loop
            gps_string = gps_string+z[9]+' '+z[10]+' '+z[11]+' '+z[12] 
            gps_data.write(gps_string+'\n')
            gps_string=''
            for row in z:
                if(row==z[12]):
                    normal.write(str(row))
                else:
                    normal.write(str(row) + ',')
            normal.write('\n')
            gps_data.close()
            fp.close()
            normal.close()
            if((int(z[6])==1) & (flag==0)):
                ip.write(sent[0]) #Debugging mode
                #time.sleep(0.500)
                print("Debugging/Caliberation data from sensors: ")
                print(ip.read())
                print("Satisfied? ")
                flag=input() #input anything other than 0
            else:
                ip.write(sent[1]) #Acknowledgement"""
        except:
            print(ValueError)
        #print (z) #just for the test run"""
        z[:]=[]
        i += 1
    db.close()

def telemetry_start():
    ip.write(sent[2]) #Start the telemetry

def telemetry_stop():
    ip.write(sent[3]) #End telemetry
    
def detach():
    ip.write(sent[4]) #Detach the mechanism

if __name__=="__main__":
    main()
    

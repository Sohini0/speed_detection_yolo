import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import dist
import tkinter as tk
from tkinter import ttk


def get_user_input():
    user_input = []

    def submit():
        # Function to be called when the user clicks the submit button
        user_input.append(entry1.get())
        user_input.append(entry2.get())
        user_input.append(entry3.get())
        user_input.append(entry4.get())
        user_input.append(entry5.get())
        user_input.append(entry6.get())
        user_input.append(entry7.get())
        window.destroy()

    # Create the main window
    window = tk.Tk()
    window.title("User Input GUI")

    # Create entry widgets for six parameters
    entry1_label = tk.Label(window, text="Video Path:")
    entry1_label.grid(row=0, column=0, padx=10, pady=5)
    entry1 = tk.Entry(window)
    entry1.grid(row=0, column=1, padx=10, pady=5)

    entry2_label = tk.Label(window, text="Sender Email:")
    entry2_label.grid(row=1, column=0, padx=10, pady=5)
    entry2 = tk.Entry(window)
    entry2.grid(row=1, column=1, padx=10, pady=5)

    entry3_label = tk.Label(window, text="Api Key:")
    entry3_label.grid(row=2, column=0, padx=10, pady=5)
    entry3 = tk.Entry(window)
    entry3.grid(row=2, column=1, padx=10, pady=5)

    entry4_label = tk.Label(window, text="Reciver Email:")
    entry4_label.grid(row=3, column=0, padx=10, pady=5)
    entry4 = tk.Entry(window)
    entry4.grid(row=3, column=1, padx=10, pady=5)

    entry5_label = tk.Label(window, text="Mail Freq:")
    entry5_label.grid(row=4, column=0, padx=10, pady=5)
    entry5 = tk.Entry(window)
    entry5.grid(row=4, column=1, padx=10, pady=5)

    entry6_label = tk.Label(window, text="Spd Dist:")
    entry6_label.grid(row=5, column=0, padx=10, pady=5)
    entry6 = tk.Entry(window)
    entry6.grid(row=5, column=1, padx=10, pady=5)

    entry7_label = tk.Label(window, text="Speed Limit:")
    entry7_label.grid(row=6, column=0, padx=10, pady=5)
    entry7 = tk.Entry(window)
    entry7.grid(row=6, column=1, padx=10, pady=5)

    # Create a submit button
    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Run the GUI application
    window.mainloop()

    return user_input

def get_video_length(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not video_capture.isOpened():
        print("Error: Couldn't open the video file.")
        return None

    # Get total number of frames
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get frames per second (fps)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Calculate video length in seconds
    video_length_seconds = total_frames / fps

    # Release the video capture object
    video_capture.release()

    return video_length_seconds

def mail(result):
    c_dwn=result[0]
    c_up=result[1]
    c_spd=result[2]
    b_dwn=result[3]
    b_up=result[4]
    b_spd=result[5]
    t_dwn=result[6]
    t_up=result[7]
    t_spd=result[8]
    # Email configuration
    sender_email = sender
    sender_password = key
    receiver_email = reciver
    subject = "Traffic Details"
    car = "Total number of car:"+str(c_up+c_dwn)+"\nUpwards Car:"+str(c_up)+"\nDownwards Car:"+str(c_dwn)+"\nOver Speeding car:"+str(c_spd)
    bus = "\nTotal number of bus:"+str(b_up+b_dwn)+"\nUpwards Car:"+str(b_up)+"\nDownwards Car:"+str(b_dwn)+"\nOver Speeding car:"+str(b_spd)
    truck = "\nTotal number of truck:"+str(t_up+t_dwn)+"\nUpwards Car:"+str(t_up)+"\nDownwards Car:"+str(t_dwn)+"\nOver Speeding car:"+str(t_spd)
    content = car+bus+truck
    #print(content)
    # Create a MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # Attach the concatenated string
    body = MIMEText(content)
    message.attach(body)
    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()

def detect():
    count=0
    #car
    upcar = {}
    downcar={}
    countercarup= [] 
    countercardown = []
    countercar_ovrspeeding = []
    #bus
    upbus = {}
    downbus={}
    counterbusup= [] 
    counterbusdown = []
    counterbus_ovrspeeding = []
    #truck
    uptruck = {}
    downtruck={}
    countertruckup= [] 
    countertruckdown = []
    countertruck_ovrspeeding = []
    start_time = time.time()
    while True:    
        ret,frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame=cv2.resize(frame,(1020,500))

        results=model.predict(frame)
    #   print(results)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
    #    print(px)
        listc=[]
        listb=[]
        listt=[]        
        
        for index,row in px.iterrows():
    #        print(row)
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=int(row[5])
            c=class_list[d]
            if 'car' in c:
                listc.append([x1,y1,x2,y2])
            elif 'bus' in c:
                listb.append([x1,y1,x2,y2])
            elif 'truck' in c:
                listt.append([x1,y1,x2,y2])
                        
        bbox_idc=trackerc.update(listc)
        bbox_idb=trackerb.update(listb)
        bbox_idt=trackert.update(listt)
        #car
        for bbox in bbox_idc:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
            cv2.putText(frame,"car",(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
            #for car going up
            if cy1 < (cy + offset) and cy1 > (cy - offset):
                upcar[id] = time.time() #to get the current time when the veh touches line1
            if id in upcar:
                if cy2 < (cy + offset) and cy2 > (cy - offset):
                    #here time.time() is the current time when veh touches L2
                    elapsed_time = time.time() - upcar[id] #to get the time in the area 
                    if countercarup.count(id) == 0: #to resolve retative count
                        countercarup.append(id)
                        a_speed_ms = distance / elapsed_time
                        a_speed_kh = a_speed_ms * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
                            countercar_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(205,120,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)      
            #car going down      
            if cy2 < (cy + offset) and cy2 > (cy - offset):
                downcar[id] = time.time()
            if id in downcar:
                if cy1 < (cy + offset) and cy1 > (cy - offset):
                    elapsed1_time = time.time() - downcar[id]
                    if countercardown.count(id) == 0:
                        countercardown.append(id)
                        a_speed_ms1 = distance / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh1>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
                            countercar_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1) 
                    cv2.putText(frame,str(int(a_speed_kh1)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        #bus
        for bbox in bbox_idb:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
            cv2.putText(frame,"bus",(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
            #for bus going up
            if cy1 < (cy + offset) and cy1 > (cy - offset):
                upbus[id] = time.time() #to get the current time when the veh touches line1
            if id in upbus:
                if cy2 < (cy + offset) and cy2 > (cy - offset):
                    #here time.time() is the current time when veh touches L2
                    elapsed_time = time.time() - upbus[id] #to get the time in the area 
                    if counterbusup.count(id) == 0: #to resolve retative count
                        counterbusup.append(id)
                        a_speed_ms = distance / elapsed_time
                        a_speed_kh = a_speed_ms * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
                            counterbus_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)        
            #bus going down      
            if cy2 < (cy + offset) and cy2 > (cy - offset):
                downbus[id] = time.time()
            if id in downbus:
                if cy1 < (cy + offset) and cy1 > (cy - offset):
                    elapsed1_time = time.time() - downbus[id]
                    if counterbusdown.count(id) == 0:
                        counterbusdown.append(id)
                        a_speed_ms1 = distance / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh1>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
                            counterbus_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1) 
                    cv2.putText(frame,str(int(a_speed_kh1)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        #truck
        for bbox in bbox_idt:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
            cv2.putText(frame,"truck",(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
            #for truck going up
            if cy1 < (cy + offset) and cy1 > (cy - offset):
                uptruck[id] = time.time() #to get the current time when the veh touches line1
            if id in uptruck:
                if cy2 < (cy + offset) and cy2 > (cy - offset):
                    #here time.time() is the current time when veh touches L2
                    elapsed_time = time.time() - uptruck[id] #to get the time in the area 
                    if countertruckup.count(id) == 0: #to resolve retative count
                        countertruckup.append(id)
                        a_speed_ms = distance / elapsed_time
                        a_speed_kh = a_speed_ms * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
                            countertruck_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)       
            #truck going down      
            if cy2 < (cy + offset) and cy2 > (cy - offset):
                downtruck[id] = time.time()
            if id in downtruck:
                if cy1 < (cy + offset) and cy1 > (cy - offset):
                    elapsed1_time = time.time() - downtruck[id]
                    if countertruckdown.count(id) == 0:
                        countertruckdown.append(id)
                        a_speed_ms1 = distance / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        if(a_speed_kh1>spd_lim):
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                            cv2.putText(frame,("Overspeeding"),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
                            countertruck_ovrspeeding.append(id)
                        else:
                            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                    #cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,255),1) 
                    cv2.putText(frame,str(int(a_speed_kh1)) + 'Km/h',(x4, y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)                                
            
        cv2.line(frame,(100,cy1),(800,cy1),(255,0,0),3)
        cv2.line(frame,(167,cy2),(680,cy2),(255,0,0),3)
        #car
        #going down
        car_down = (len(countercardown))
        cv2.putText(frame,('Car Going down:') + str(car_down),(745,40),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #For going up
        car_up = (len(countercarup))
        cv2.putText(frame,('Car Going up :') + str(car_up),(745,70),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #over speeding
        car_spd =len(countercar_ovrspeeding)
        cv2.putText(frame,'Car Overspeeding:' + str(car_spd),(10,40),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
        #bus
        #going down
        bus_down = (len(counterbusdown))
        cv2.putText(frame,('Bus Going down:') + str(bus_down),(745,100),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #For going up
        bus_up = (len(counterbusup))
        cv2.putText(frame,('Bus Going up:') + str(bus_up),(745,130),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #over speeding
        bus_spd =len(counterbus_ovrspeeding)
        cv2.putText(frame,'Bus Overspeeding:' + str(bus_spd),(10,65),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
        #truck
        #going down
        truck_down = (len(countertruckdown))
        cv2.putText(frame,('Truck Going down:') + str(truck_down),(745,160),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #For going up
        truck_up = (len(countertruckup))
        cv2.putText(frame,('Truck Going up:') + str(truck_up),(745,190),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)
        #overspeeding
        truck_spd =len(countertruck_ovrspeeding)
        cv2.putText(frame,'Truck Overspeeding:' + str(truck_spd),(10,90),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

        Result = [car_down, car_up, car_spd, bus_down, bus_up, bus_spd, truck_down, truck_up, truck_spd]

        cv2.imshow("RGB", frame)
        cv2.waitKey(1)

        if path==0:
            if t_time/60==freq:
                mail(Result)
    end_time = time.time()
    t_time = (end_time - start_time)
    print(t_time)
    vid_time=get_video_length(path)
    print(vid_time)
    #print(Result)
    if path != 0:
        if t_time >= vid_time:
            mail(Result)

if __name__ == "__main__":
    uin=get_user_input()
    model = YOLO('yolov7.pt')
    def RGB(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE :  
            colorsBGR = [x, y]
            print(colorsBGR)
            
    cv2.namedWindow('RGB')
    cv2.setMouseCallback('RGB', RGB)
    if uin[0]==0:
        path=0
    else:
        path=uin[0]
    cap=cv2.VideoCapture(path)
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n") 
    #print(class_list)
    trackerc=Tracker()
    trackerb=Tracker()
    trackert=Tracker()
    cy1=260
    cy2=156
    offset=6
    distance=int(uin[5])
    spd_lim=int(uin[6])
    sender=uin[1]
    key=uin[2]
    reciver=uin[3]
    freq=int(uin[4])
    car_down=0
    car_up=0
    car_spd=0
    bus_down=0
    bus_up=0
    bus_spd=0
    truck_down=0
    truck_up=0
    truck_spd=0
    a_speed_kh=0
    detect()
    
cap.release()
cv2.destroyAllWindows()
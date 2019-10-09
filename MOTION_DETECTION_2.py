import cv2
import glob
import xlrd
import pandas
from datetime import datetime
#import Video_Data_Ploting

''' Motion recognition on Video'''
''' py -3  MOTION_DETECTION.py '''

#Cach first frame from camera - Catturo prima immagine
video=cv2.VideoCapture(0) # da telecamera -= Camera source
    #face=face_castade.detectMultiScale(img_Gr,scaleFactor=1.05,minNeighbors=5)
Time_t      = 1
Frame_numb  = 1
fist_frame  = None

status_list = [None,None]
tims_list   = []
df          = pandas.DataFrame(columns=["Start","End"])     #Data_Frame
while True:
    check,frame = video.read()
    frame_Gr    = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #conversione in Grigio
    frame_Gr    = cv2.GaussianBlur(frame_Gr,(21,21),0)
    status      = 0

    if fist_frame is None:
       fist_frame = frame_Gr
       continue

    delta_frame = cv2.absdiff(fist_frame,frame_Gr)

    #converto spbra na certa scaladi grigi i pixel in bianco gli altri in nero
    #grey pixel over 30% treashold will be converted in white, the rest in Blck
    thresh_frame = cv2.threshold(delta_frame, 50 , 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("threash_IMG_A",thresh_frame) # CHECK OUTPUT
    # riduco le parti bianche inutili, o le converto in Black - iterations=2 quante volte riprete il processo
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Cercando i contorni - searching contours
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for Contours in cnts:
        if cv2.contourArea(Contours) < 1200:
             continue
        status  = 1

        x,y,w,z = cv2.boundingRect(Contours)
        frame   = cv2.rectangle(frame,(x,y),(x+w,y+z),( 0,255,0),3)

        #Topo / Orsacchiotto
        #frame = cv2.circle(frame,(x,(y-5)),30,( 0,255,0),3)
        #frame = cv2.circle(frame,(x+w,(y-5)),30,( 0,255,0),3)
        #frame = cv2.circle(frame,(x+(w//2),y+(z//2)),90,( 0,255,0),3)
        #frame = cv2.circle(frame,(x+(w//2),y+(z//2)),10,( 0,255,0),3)
    status_list.append( status )

    status_list = status_list[-2:]


    if status_list[-1] == 1 and status_list[-2] == 0:
        tims_list.append(datetime.now())

    if status_list[-1] == 0 and status_list[-2] == 1:
        tims_list.append(datetime.now())

    #cv2.imshow("DELTA_IMG",delta_frame)         # CHECK OUTPUT
    #cv2.imshow("GRAY_IMG",frame_Gr)             # CHECK OUTPUT
    #cv2.imshow("threash_IMG",thresh_frame)      # CHECK OUTPUT
    cv2.imshow("threash_IMG",frame)              # CHECK OUTPUT
    key=cv2.waitKey(Time_t)

        #for x,y,w,z in face:
            #frame = cv2.rectangle(frame,(x,y),(x+w,y+z),( 0,255,0),3)

    if key == ord('q'):  #esce loop in caso utente preme Q - press Q to exit loop
       if status == 1:
          tims_list.append(datetime.now())
       break

print( status_list )
print( tims_list )

for i in range(0,len(tims_list),2):
    df=df.append({"Start":tims_list[i] , "End":tims_list[i+1]},ignore_index=True)

df.to_csv("new_CSV_FILE.csv") #scrvo Dataframe su file


#print('Programma interrotto \n Numero di frame analizzati : '+ str(Frame_numb))
video.release() # per rilascio utilizzo camera - release camera utilization
cv2.destroyAllWindows()

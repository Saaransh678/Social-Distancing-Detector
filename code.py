from cv2 import cv2

import math 


class Point(): 
	def __init__(self, x, y): 
		self.x = x 
		self.y = y 

def dist(p1, p2): 
	return math.sqrt((p1.x - p2.x) *
					(p1.x - p2.x) +
					(p1.y - p2.y) *
					(p1.y - p2.y)) 


def bruteForce(P, n): 
	min_val = float('inf') 
	for i in range(n): 
		for j in range(i + 1, n): 
			if dist(P[i], P[j]) < min_val: 
				min_val = dist(P[i], P[j]) 

	return min_val 
def stripClosest(strip, size, d): 
	
	
	min_val = d 

	strip.sort(key = lambda point: point.y) 

	
	for i in range(size): 
		j = i + 1
		while j < size and (strip[j].y -
							strip[i].y) < min_val: 
			min_val = dist(strip[i], strip[j]) 
			j += 1

	return min_val 


def closestUtil(P, n): 
	

	if n <= 3: 
		return bruteForce(P, n) 
	mid = n // 2
	midPoint = P[mid]  
	dl = closestUtil(P[:mid], mid) 
	dr = closestUtil(P[mid:], n - mid) 

	
	d = min(dl, dr) 

	
	strip = [] 
	for i in range(n): 
		if abs(P[i].x - midPoint.x) < d: 
			strip.append(P[i]) 

	 
	return min(d, stripClosest(strip, len(strip), d)) 


def closest(P, n): 
	P.sort(key = lambda point: point.x) 

	 
	return closestUtil(P, n) 


face_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cap = cv2.VideoCapture('sample2.webm')

while cap.isOpened():
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    p=[]
    for (x, y , w ,h) in faces:
        p.append(Point(x+w/2,y+h/2))
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0 , 0), 3)
    n=len(p)
    font=cv2.FONT_HERSHEY_COMPLEX
    if closest(p,n)>200:
        cv2.putText(img,"social distancing following",(23,67),font,1,(0,255,0),2,cv2.LINE_AA)
    else:
        cv2.putText(img,"social distancing not following",(23,67),font,1,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

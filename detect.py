import cv2
import mediapipe as mp
from scipy.spatial import distance
import pygame

#initialize pygame mixer for alarm sound
pygame.mixer.init()  # pygame.mixer is a module in the Pygame library that provides functionality for loading and playing sound files. 

#load alarm sound
alarm_sound = pygame.mixer.Sound("warning.wav")   # Sound() is used to load a sound file to memory so that it can be played later.


# initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()  # FaceMesh() is a class that loads the Face Mesh AI model. It provides methods for processing images and extracting facial landmarks.

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

#open webcam
cap = cv2.VideoCapture(0)

#counter for drowsiness detection
counter = 0  #to count how many consecutive frames the eyes remain closed.

#EAR calculation function
def calculate_EAR(eye_points):   #euclidean() is a function from the scipy library. It calculates the straight-line distance between two points.
    A = distance.euclidean(eye_points[1], eye_points[5])  #vertical eye height
    B = distance.euclidean(eye_points[2], eye_points[4])  #another vertical eye height
    C = distance.euclidean(eye_points[0], eye_points[3])  #eye width

    EAR = (A + B) / (2.0 * C)

    return EAR

while True:
    ret, frame = cap.read()

    if not ret:
        break

    #flip webcam
    frame = cv2.flip(frame, 1)

    #convert the image BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #process the RGB image to get the face mesh landmarks
    results = face_mesh.process(rgb_frame)

    h, w, c = frame.shape  #h= height, w= width, c= channels of the frame

    #draw the face mesh landmarks on the original frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            left_eye_points = []
            right_eye_points = []

            #left eye landmarks
            for i in LEFT_EYE:
                landmark = face_landmarks.landmark[i]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                left_eye_points.append((x, y))

                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)   #cv2.circle(image, center, radius, color, thickness)

            #right eye landmarks
            for i in RIGHT_EYE:
                landmark = face_landmarks.landmark[i]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                right_eye_points.append((x, y))

                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            #calculate EAR for both eyes
            if len(left_eye_points) == 6 and len(right_eye_points) == 6:

                left_EAR = calculate_EAR(left_eye_points)
                right_EAR = calculate_EAR(right_eye_points)

                avg_EAR = (left_EAR + right_EAR) / 2.0

                #display EAR
                cv2.putText(frame, f'EAR: {avg_EAR: 2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                #drowsiness detection
                if avg_EAR < 0.20:

                    counter += 1

                    #show eye closed status
                    cv2.putText(frame, 'EYES CLOSED', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    if counter > 30:

                        cv2.putText(frame, 'DRIVER IS SLEEPY', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                        if not pygame.mixer.get_busy():
                            alarm_sound.play()
                else:
                    counter = 0

                    #show eye open status
                    cv2.putText(frame, 'EYES OPEN', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow('Driver Drowsiness', frame)

    #press ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
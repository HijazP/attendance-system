import cv2
import numpy as np
import tensorflow as tf
# Load the trained model
model = tf.keras.models.load_model('face_recognition_model.h5')

# Function to preprocess the image for prediction
def preprocess_image(img):
    img = cv2.resize(img, (100, 100))  # Sesuaikan dengan input model
    img = img / 255.0  # Normalisasi
    img = np.expand_dims(img, axis=0)
    return img

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Dictionary mapping class IDs to names
id_to_name = {
    0: 'Alice',
    1: 'Bob',
    2: 'Charlie',
    3: 'David',
    4: 'Eve',
    5: 'Frank',
    6: 'Grace',
    7: 'Hank',
    8: 'Ivy',
    9: 'Jack',
    10: 'Kathy',
    11: 'Leo',
    12: 'Mona',
    13: 'Nina',
    14: 'Oscar',
    15: 'Pam',
    16: 'Quinn'
}

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Loop over the faces detected
    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face = frame[y:y+h, x:x+w]
        
        # Preprocess the face for the model
        processed_face = preprocess_image(face)
        
        # Make a prediction
        prediction = model.predict(processed_face)
        class_id = np.argmax(prediction)
        
        # Get the name corresponding to the class ID
        name = id_to_name.get(class_id, 'Unknown')
        
        # Display the results on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

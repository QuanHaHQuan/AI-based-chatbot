import face_recognition
import cv2
import numpy as np
import matplotlib as plt

def recognition():
    apply_face_encodings = []
    apply_face_locations = []
    known_face_encodings = []

    cap = cv2.VideoCapture(0)
    i = 0

    while(1):
        ret, frame = cap.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        apply_face_locations = face_recognition.face_locations(rgb_small_frame)
        apply_face_encodings = face_recognition.face_encodings(rgb_small_frame, apply_face_locations)
        
        if len(apply_face_encodings) == 0:
            i += 1
            if (i % 50 == 0):
                print("there is no face in the picture!")
            
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
            
    names = [
        "quan",
        "bo",
        "zhang",
        "liu"]

    images = []

    for name in names:
        filename = "./facial_info/" + name + ".jpg"
        image = face_recognition.load_image_file(filename)
        images.append(image)

    for image in images:
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

    face_names = []

    for apply_face_encoding in apply_face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, apply_face_encoding)
        name = "Stranger"

        face_distances = face_recognition.face_distance(known_face_encodings, apply_face_encoding)
        best_match_index = np.argmin(face_distances)
        res = min(face_distances)
        if(res > 0.55):
            face_names.append(name)
        elif matches[best_match_index]:
            name = names[best_match_index]
            face_names.append(name)
        else:
            face_names.append(name)
    return face_names[0]
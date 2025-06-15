from ultralytics import YOLO
import cv2

model = YOLO("model/yolov8n-face.pt")  

def detect_faces(image_path):
    image = cv2.imread(image_path)

    results = model(image)[0]
    face_count = 0

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]

        if conf > 0.3:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 4)
            face_crop = image[y1:y2, x1:x2]
            face_filename = f"static/face_{face_count}.jpg"
            cv2.imwrite(face_filename, face_crop)
            cv2.putText(image, f'{int(conf * 100)}%', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            face_count += 1


    output_path = "static/detected.jpg"
    cv2.imwrite(output_path, image)

    return output_path, face_count

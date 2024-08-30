from ultralytics import YOLO
import cv2
from windowcapture import WindowCapture
from collections import defaultdict
import numpy as np
import torch

offset_x = 945
offset_y = 200

wincap = WindowCapture(size=(910, 620), origin=(offset_x, offset_y))
#wincap = WindowCapture("Minecraft 1.7.10")

#model = YOLO("yolov8s.pt")
model = YOLO(r"C:\Users\leona\OneDrive\Documents\GitHub\Inteligencia_Artificial\runs\detect\train\weights\best.pt")

track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

while True:
    img = wincap.get_screenshot()

    if seguir:
        results = model.track(img, persist=True)
    else:
        results = model(img)

    for result in results:
        try:
            if not torch.isnan(result.boxes.xywh).any():
                img = result.plot()
            else:
                print("Caixa com coordenadas inválidas detectada, pulando a plotagem.")
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")

        if seguir and deixar_rastro:
            try:
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()

                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    if not np.isnan(x) and not np.isnan(y):
                        track = track_history[track_id]
                        track.append((float(x), float(y)))
                        if len(track) > 30:
                            track.pop(0)

                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)
            except Exception as e:
                print(f"Erro ao processar rastreamento: {e}")

    cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
print("desligando")

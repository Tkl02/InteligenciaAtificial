from ultralytics import YOLO

caminho = r"C:\Users\leona\OneDrive\Documents\GitHub\Inteligencia_Artificial\trabalhofinal\mine.yaml"

# modelos Yolo
# Model	    size    mAPval  Speed       Speed       params  FLOPs
#           (pixels) 50-95  CPU ONNX A100 TensorRT   (M)     (B)
#                           (ms)        (ms)
# YOLOv8n	640	    37.3	80.4	    0.99	    3.2	    8.7
# YOLOv8s	640	    44.9	128.4	    1.20	    11.2	28.6
# YOLOv8m	640	    50.2	234.7	    1.83	    25.9	78.9
# YOLOv8l	640	    52.9	375.2	    2.39	    43.7	165.2
# YOLOv8x	640	    53.9	479.1	    3.53	    68.2	257.8

def main():
    model = YOLO("yolov8x.pt")
    model.train(data=caminho, epochs=50, device=0)

if __name__ == '__main__':
    main()
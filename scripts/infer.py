import cv2
from ultralytics import YOLO


def main():
    model = YOLO("runs/detect/train8/weights/best.pt")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame.")
            break

        # Executa a inferência no frame
        # O método retorna uma lista de resultados, onde cada elemento é uma imagem com as anotações desenhadas.
        # Certifique-se que o dispositivo esteja configurado corretamente
        results = model(frame, device="cuda")
        annotated_frame = results.render()[0]

        # Exibe o frame anotado
        cv2.imshow("Detecção de EPIs - Webcam", annotated_frame)

        # Se a tecla 'q' for pressionada, encerra o loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

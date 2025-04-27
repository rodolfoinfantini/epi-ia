import cv2 as cv
import argparse
from ultralytics import YOLO
from overlap import check_overlap


def main(args):
    print(f"Carregando modelo {args.model}...")
    model = YOLO(f"runs/detect/{args.model}/weights/best.pt")
    cv.namedWindow("preview")
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame.")
            break

        # Executa a inferência no frame
        # O método retorna uma lista de resultados, onde cada elemento é uma imagem com as anotações desenhadas.
        # Certifique-se que o dispositivo esteja configurado corretamente

        # frame_pil = Image.fromarray(frame)
        results = model(frame, device=args.device)
        check_overlap(frame, results[0])

        annotated_frame = results[0].plot()

        # Exibe o frame anotado
        cv.imshow("preview", annotated_frame)

        # Se a tecla 'q' for pressionada, encerra o loop
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyWindow("preview")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execução do modelo de detecção de EPIs com YOLOv8")
    parser.add_argument("--model", type=str, default="train8",
                        help="Modelo treinado (default: train8)")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Dispositivo (ex.: 'cuda' ou 'cpu', default: cuda)")
    args = parser.parse_args()
    main(args)

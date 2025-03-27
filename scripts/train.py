# train.py
import argparse
from ultralytics import YOLO


def main(args):
    model = YOLO(args.model)

    print(f"Iniciando o treinamento com {args.epochs} épocas...")
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.img_size,
        device=args.device,
        batch=args.batch_size,
        save_dir="E:/dev/puc/epi-ia/logs"
    )

    print("Treinamento concluído!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Treinamento do modelo de detecção de EPIs com YOLOv8")
    parser.add_argument("--data", type=str, default="data/datasets.yaml",
                        help="Caminho para o arquivo de configuração do dataset (ex.: data/datasets.yaml)")
    parser.add_argument("--epochs", type=int, default=50,
                        help="Número de épocas de treinamento (default: 50)")
    parser.add_argument("--img_size", type=int, default=640,
                        help="Tamanho da imagem (resolução de entrada, default: 640)")
    parser.add_argument("--batch_size", type=int, default=16,
                        help="Tamanho do batch de treinamento (default: 16)")
    parser.add_argument("--model", type=str, default="yolov8n.pt",
                        help="Modelo pré-treinado para fine-tuning (default: yolov8n.pt)")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Dispositivo para treinamento (ex.: 'cuda' ou 'cpu', default: cuda)")
    args = parser.parse_args()
    main(args)

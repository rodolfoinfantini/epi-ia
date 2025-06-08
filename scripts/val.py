import argparse
from ultralytics import YOLO

def main(args):
    model = YOLO(f"runs/detect/{args.model}/weights/best.pt")
    model.val(data=args.data, batch=1, imgsz=args.img_size, device=args.device)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validação")
    parser.add_argument("--model", type=str, default="train4")
    parser.add_argument("--data", type=str, default="data/datasets.yaml")
    parser.add_argument("--img_size", type=int, default=840)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()
    main(args)

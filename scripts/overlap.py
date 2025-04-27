from typing import List, Tuple, Dict
from alert_debouncer import AlertDebouncer
import numpy as np
import cv2 as cv

# 2 segundos de persistência
debouncer = AlertDebouncer(persist_time=3.0, iou_thresh=0.5)

overlay_pipelines = [['Person', 'Face', 'Glasses'],
                     ['Person', 'Head', 'Helmet']]
conf_threshold = {
    'Person': 0.6,
    'Face': 0.6,
    'Glasses': 0.4,
    'Head': 0.5,
    'Helmet': 0.5
}


def filter_predictions(res, conf_threshold: Dict) -> List[Tuple[List[float], str, float]]:
    boxes = res.boxes
    xyxy = boxes.xyxy.cpu().numpy()
    cls_ids = boxes.cls.cpu().numpy().astype(int)
    confs = boxes.conf.cpu().numpy()

    filtered = []
    for box, cls_id, conf in zip(xyxy, cls_ids, confs):
        class_name = res.names[cls_id]
        threshold = conf_threshold.get(class_name, 0.0)
        if conf >= threshold:
            filtered.append((box.tolist(), class_name, float(conf)))
    return filtered


def check_overlap(image, results):
    preds = filter_predictions(results, conf_threshold)
    alerts = run_overlap_pipelines(preds, overlay_pipelines)
    confirmed = debouncer.update(alerts)
    print(confirmed)


def has_overlap(a, b) -> bool:
    return (a[0] <= b[2] and a[2] >= b[0]     # projeção X se sobrepõe
            and a[1] <= b[3] and a[3] >= b[1])     # projeção Y se sobrepõe


def run_overlap_pipelines(
    preds: List[Tuple[List[float], str, float]],
    pipelines: List[List[str]]
) -> List[Dict]:
    """
    preds: lista de (box, class_name, conf)
    pipelines: listas de sequência de classes, ex [['Person','Face','Glasses'], ...]
    Retorna lista de alertas: { 'pipeline': [...], 'start_box': [...], 'missing': 'Class' }
    """
    # Converte preds em arrays e listas paralelas
    boxes = np.array([p[0] for p in preds])    # shape (M,4)
    cls_names = [p[1] for p in preds]           # shape (M,)
    alerts = []

    # Para cada pipeline
    for pipeline in pipelines:
        idxs_by_name = {name: np.where(np.array(cls_names) == name)[0]
                        for name in pipeline if name in cls_names}

        first = pipeline[0]
        for i in idxs_by_name.get(first, []):
            start_box = boxes[i]
            current_indices = [i]

            # percorre cada etapa seguinte
            for step in pipeline[1:]:
                if step not in idxs_by_name:
                    # se for a última etapa, gera alerta
                    if step == pipeline[-1]:
                        alerts.append({
                            'pipeline': pipeline,
                            'start_box': start_box.tolist(),
                            'missing': step
                        })
                    break

                # busca todas as caixas dessa etapa que sobrepõem
                next_indices = []
                for ci in current_indices:
                    for j in idxs_by_name[step]:
                        if has_overlap(start_box, boxes[j]):
                            next_indices.append(j)
                if not next_indices:
                    if step == pipeline[-1]:
                        alerts.append({
                            'pipeline': pipeline,
                            'start_box': start_box.tolist(),
                            'missing': step
                        })
                    break
                # para etapas intermediárias, segue apenas se encontrou
                current_indices = next_indices

    return alerts

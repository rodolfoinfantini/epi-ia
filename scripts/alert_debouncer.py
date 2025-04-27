import time
from typing import Dict, Tuple


def iou(a, b):
    # a, b: [x1,y1,x2,y2]
    xi1 = max(a[0], b[0])
    yi1 = max(a[1], b[1])
    xi2 = min(a[2], b[2])
    yi2 = min(a[3], b[3])
    inter = max(0, xi2-xi1) * max(0, yi2-yi1)
    area_a = (a[2]-a[0])*(a[3]-a[1])
    area_b = (b[2]-b[0])*(b[3]-b[1])
    union = area_a + area_b - inter
    return inter/union if union > 0 else 0


class AlertDebouncer:
    def __init__(self, persist_time: float, iou_thresh: float = 0.5):
        self.persist_time = persist_time
        self.iou_thresh = iou_thresh
        # cada entrada é um dict com keys: pipeline, missing, first_seen, last_seen, box
        self.entities = []

    def update(self, raw_alerts):
        now = time.time()
        confirmed = []

        # 1) para cada alerta bruto, tente encaixar em uma entidade existente
        for alert in raw_alerts:
            box = alert['start_box']
            pipeline = tuple(alert['pipeline'])
            missing = alert['missing']

            # procura entidade compatível
            matched = None
            for ent in self.entities:
                if ent['pipeline'] == pipeline and ent['missing'] == missing:
                    if iou(ent['box'], box) >= self.iou_thresh:
                        matched = ent
                        break

            if matched:
                # atualiza last_seen e usa box mais recente (ou média, se quiser)
                matched['last_seen'] = now
                matched['box'] = box
            else:
                # cria nova entidade
                self.entities.append({
                    'pipeline': pipeline,
                    'missing': missing,
                    'first_seen': now,
                    'last_seen': now,
                    'box': box
                })

        # 2) verifica quais entidades persistiram e quais expiraram
        for ent in list(self.entities):
            duration = ent['last_seen'] - ent['first_seen']
            if duration >= self.persist_time:
                # confirme esse alerta e remova a entidade para não repetir
                confirmed.append({
                    'pipeline': list(ent['pipeline']),
                    'missing': ent['missing'],
                    'start_box': ent['box']
                })
                self.entities.remove(ent)
            else:
                # se não vimos esse alerta há muito tempo, descartamos
                if now - ent['last_seen'] > self.persist_time:
                    self.entities.remove(ent)

        return confirmed

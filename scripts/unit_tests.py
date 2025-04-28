from overlap import has_overlap
from database import save_alert


def has_overlap_test():
    tests = [
        # 1. Testes originais
        ([139.9892, 196.0672, 545.0209, 479.7748],
         [231.1768, 238.6934, 350.7286, 384.5688], True),
        # invertido
        ([231.1768, 238.6934, 350.7286, 384.5688],
         [139.9892, 196.0672, 545.0209, 479.7748], True),
        # sem overlap
        ([50, 50, 100, 100], [150, 150, 200, 200], False),
        # overlap parcial
        ([50, 50, 100, 100], [75, 75, 125, 125], True),
        # toque de borda
        ([50, 50, 100, 100], [100, 100, 150, 150], True),
        # idênticas
        ([50, 50, 100, 100], [50, 50, 100, 100], True),
        # contenção simples
        ([0, 0, 100, 100], [50, 50, 150, 150], True),
        # borda em 0
        ([0, 0, 100, 100], [100, 100, 200, 200], True),
        # idênticas no zero
        ([0, 0, 100, 100], [0, 0, 100, 100], True),
        # disjuntas absolutas
        ([0, 0, 100, 100], [200, 200, 300, 300], False),
        # contida interna
        ([0, 0, 100, 100], [50, 50, 75, 75], True),

        # 2. “Cruz” — overlap sem canto interno
        # deve ser True, mas a sua fun falha
        ([0, 40, 100, 60], [40, 0, 60, 100], True),

        # 3. Caixas degeneradas (zero-area)
        ([0, 0, 0, 100], [0, 50, 0, 150], True),     # linha vertical coincide
        ([0, 0, 100, 0], [50, 0, 150, 0], True),     # linha horizontal

        # 4. Coordenadas negativas
        ([-50, -50, 50, 50], [0, 0, 100, 100], True),
        ([-50, -50, -10, -10], [0, 0, 100, 100], False),

        # 5. Parcialmente deslocadas
        ([10, 10, 20, 20], [5, 5, 15, 15], True),
        ([10, 10, 20, 20], [20, 20, 30, 30], True),

        # 6. Grandes diferenças
        ([0, 0, 100, 100], [1000, 1000, 1100, 1100], False),
    ]

    for xy1, xy2, expected in tests:
        result = has_overlap(xy1, xy2)
        status = "OK" if result == expected else "FAIL"
        print(f"{xy1=} {xy2=} → esperado={
              expected}, obtido={result} [{status}]")


def save_alert_test():
    tests = [
        {
            'alert_class': 'Glasses',
            'timestamp': '20250427_204000',
            'filename': 'recordings/Glasses_20250427_204000.mp4',
        },
        {
            'alert_class': 'Helmet',
            'timestamp': '20250427_204500',
            'filename': 'recordings/Helmet_20250427_204500.mp4',
        },
    ]

    for test in tests:
        alert_class = test['alert_class']
        timestamp = test['timestamp']
        filename = test['filename']

        save_alert(alert_class, timestamp, filename)


has_overlap_test()
save_alert_test()

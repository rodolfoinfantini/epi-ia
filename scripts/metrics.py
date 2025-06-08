import matplotlib.pyplot as plt
import pandas as pd
import os

runs = ['1', '2', '3', '4']
dfs = []
save_folder = 'metrics'

for run in runs:
    folder = f'runs/detect/train{run}'
    csv_path = os.path.join(folder, 'results.csv')
    args_path = os.path.join(folder, 'args.yaml')
    if os.path.isfile(csv_path) and os.path.isfile(args_path):
        df = pd.read_csv(csv_path, index_col=0)
        df['run'] = run
        # Extrai batch e imgsz de args.yaml (constantes por run)
        with open(args_path, 'r') as f:
            batch = None
            imgsz = None
            for line in f:
                if 'batch:' in line:
                    batch = int(line.split(':')[1].strip())
                elif 'imgsz:' in line:
                    imgsz = int(line.split(':')[1].strip())
        df['batch'] = batch
        df['imgsz'] = imgsz
        dfs.append(df)
    else:
        print(f"Aviso: não encontrou {csv_path} ou {args_path}")

if not dfs:
    raise RuntimeError(
        "Nenhum results.csv foi carregado! Verifique os caminhos.")

df_all = pd.concat(dfs, ignore_index=True)

fig, ax1 = plt.subplots(figsize=(8, 4))

for run_name, group in df_all.groupby('run'):
    epochs = group.index.values.tolist()
    ax1.plot(epochs, group['metrics/precision(B)'],
             label=f"train{run_name} – precision")

ax1.set_xlabel('Época')
ax1.set_ylabel('Precision', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Cria eixo Y secundário
ax2 = ax1.twinx()
for run_name, group in df_all.groupby('run'):
    epochs = group.index.values.tolist()
    # Como batch/imgsz são constantes, plota só o primeiro ponto para gerar linha horizontal
    b = group['batch'].iloc[0]
    i = group['imgsz'].iloc[0]
    ax2.hlines(b, xmin=epochs[0], xmax=epochs[-1],
               colors='tab:orange', linestyles='--',
               label=f"train{run_name} – batch={b}")
    ax2.hlines(i, xmin=epochs[0], xmax=epochs[-1],
               colors='tab:green', linestyles=':',
               label=f"train{run_name} – imgsz={i}")

ax2.set_ylabel('Hiperparâmetros', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Combina legendas de ambos os eixos
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='best')

plt.title('Precision (e Batch/ImgSz) vs Época')
plt.tight_layout()
plt.savefig(os.path.join(save_folder, 'precision_vs_epoch.png'))


# Recall
fig, ax1 = plt.subplots(figsize=(8, 4))

for run_name, group in df_all.groupby('run'):
    epochs = group.index.values.tolist()
    ax1.plot(epochs, group['metrics/recall(B)'],
             label=f"train{run_name} – recall")

ax1.set_xlabel('Época')
ax1.set_ylabel('Recall', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Cria eixo Y secundário para batch/imgsz
ax2 = ax1.twinx()
for run_name, group in df_all.groupby('run'):
    epochs = group.index.values.tolist()
    b = group['batch'].iloc[0]
    i = group['imgsz'].iloc[0]
    ax2.hlines(b, xmin=epochs[0], xmax=epochs[-1],
               colors='tab:orange', linestyles='--',
               label=f"train{run_name} – batch={b}")
    ax2.hlines(i, xmin=epochs[0], xmax=epochs[-1],
               colors='tab:green', linestyles=':',
               label=f"train{run_name} – imgsz={i}")

ax2.set_ylabel('Hiperparâmetros', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Combina legendas de ambos os eixos
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='best')

plt.title('Recall (e Batch/ImgSz) vs Época')
plt.tight_layout()
plt.savefig(os.path.join(save_folder, 'recall_vs_epoch.png'))

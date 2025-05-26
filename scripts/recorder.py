from typing import Tuple
import cv2 as cv
import time
import numpy as np
import subprocess
import os
import shlex


class VideoRecorder:
    """
    Envia frames em tempo real para um processo FFmpeg via stdin,
    capturando thumbnail e interrompendo após `duration` segundos.
    """

    def __init__(self,
                 filename: str,
                 duration: float,
                 frame_size: Tuple[int, int]):
        self.filename = filename
        self.duration = duration
        self.frame_size = frame_size  # (width, height)
        self.start_time = time.time()
        self.stopped = False

        # thumbnail (.png) a partir do .webm
        base, _ = os.path.splitext(filename)
        self.thumb_path = base + ".png"
        self._thumb_saved = False

        # Monta comando FFmpeg para pipe rawvideo BGR24 → WebM (VP8)
        width, height = frame_size
        cmd = (
            f'ffmpeg -y '
            f'-f rawvideo -pixel_format bgr24 '
            f'-video_size {width}x{height} '
            f'-i pipe:0 '
            f'-c:v libvpx -auto-alt-ref 0 -threads 4 '
            f'"{filename}"'
        )
        # Inicia o processo
        self.proc = subprocess.Popen(
            shlex.split(cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # notificação (opcional)
        subprocess.run(["notify-send", f"[Recorder] iniciado: {filename}"])

    def update(self, frame: np.ndarray):
        """
        Chamar a cada frame:
         - Salva thumbnail no primeiro frame
         - Passa o frame para o ffmpeg via stdin
         - Ao completar `duration`, encerra o processo
        Retorna o nome do arquivo quando finalizado, ou None.
        """
        if self.stopped:
            return None

        # salva thumb uma única vez
        if not self._thumb_saved:
            cv.imwrite(self.thumb_path, frame)
            self._thumb_saved = True

        # envia raw BGR24 para ffmpeg
        try:
            self.proc.stdin.write(frame.tobytes())
        except BrokenPipeError:
            # ffmpeg pode ter fechado; tratamos como encerrado
            self.stopped = True
            return None

        # checa duração
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            return self.stop_and_notify(elapsed)

        return None

    def stop_and_notify(self, elapsed: float):
        """Fecha stdin, espera o ffmpeg terminar e notifica."""
        if self.stopped:
            return None
        # fecha pipe e aguarda
        self.proc.stdin.close()
        self.proc.wait()
        self.stopped = True

        # notifica
        subprocess.run([
            "notify-send",
            f"[Recorder] salvo {self.filename} | tempo={elapsed:.1f}s"
        ])
        return self.filename

    def is_active(self) -> bool:
        return not self.stopped

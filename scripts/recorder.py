from typing import Tuple, List
import cv2 as cv
import time
import numpy as np
import subprocess
import os


class VideoRecorder:
    """
    Bufferiza frames por `duration` segundos, calcula o fps real
    e só então escreve o arquivo de vídeo no disco.
    """

    def __init__(self, filename: str, duration: float, frame_size: Tuple[int, int]):
        self.filename = filename
        self.duration = duration
        self.frame_size = frame_size
        self.start_time = time.time()
        self.frames: List[np.ndarray] = []
        self.stopped = False

        # Gera o caminho da thumbnail (.png) a partir do .webm
        base, _ = os.path.splitext(filename)
        self.thumb_path = base + ".png"
        self._thumb_saved = False

        subprocess.run(["notify-send", f"\"[Recorder] iniciado: {filename}\""])

    def update(self, frame: np.ndarray):
        """
        Chamar a cada frame:
         - Salva no buffer
         - Se já passou `duration`, para e escreve o arquivo
        """
        if self.stopped:
            return None

        if not self._thumb_saved:
            cv.imwrite(self.thumb_path, frame)
            self._thumb_saved = True

        self.frames.append(frame.copy())
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            return self.stop_and_write(elapsed)

        return None

    def stop_and_write(self, elapsed: float):
        """Calcula fps = len(frames)/elapsed e escreve o vídeo."""
        fps = len(self.frames) / elapsed if elapsed > 0 else 1.0
        fourcc = cv.VideoWriter_fourcc(*'VP90')
        writer = cv.VideoWriter(self.filename, fourcc, fps, self.frame_size)
        for f in self.frames:
            writer.write(f)
        writer.release()
        self.stopped = True
        subprocess.run(["notify-send", f"\"[Recorder] salvo {self.filename} | frames={len(self.frames)} | "
                        f"tempo={elapsed:.1f}s | fps={fps:.1f}\""])

        return self.filename

    def is_active(self) -> bool:
        return not self.stopped

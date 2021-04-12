from pathlib import Path
from typing import Any
import wave
from dataclasses import dataclass
from tempfile import TemporaryFile
import struct

SAMPLE_DIR = "C:\\Users\\Krasn\\Downloads\\SAMPLES\\adjusted"


@dataclass(frozen=True)
class WavParams:
    channels: int
    sample_width: int
    frame_rate: int
    frame_count: int
    compression_type: Any
    compression_name: str

    @property
    def is_valid(self):
        return (
            self.channels == 1 and self.sample_width == 2 and self.frame_rate == 44100
        )


def is_valid_wav(path: Path) -> bool:
    try:
        with wave.open(str(path), "rb") as wav:
            wav_params = WavParams(*wav.getparams())
            return wav_params.is_valid
    except EOFError:
        return False


def main():
    sample_dir = Path(SAMPLE_DIR)
    wav_files = sample_dir.glob("*.wav")
    valid_wavs = filter(is_valid_wav, wav_files)

    sample_count = 0
    data_size = 0
    sample_descriptors: list[tuple] = []

    with TemporaryFile() as tmp_file:
        offset = 0
        for wav_path in valid_wavs:
            with wave.open(str(wav_path), "rb") as wav:
                num_frames: int = wav.getnframes()
                frames: bytes = wav.readframes(num_frames)
                tmp_file.write(frames)
                sample_descriptors.append((offset, num_frames))
                data_size += num_frames * wav.getsampwidth()
                sample_count += 1
                offset += num_frames
        with open("bank", "wb") as fp:
            header = struct.pack("II", sample_count, data_size)
            fp.write(header)
            for sample_desc in sample_descriptors:
                fp.write(struct.pack("II", *sample_desc))
            tmp_file.seek(0)
            fp.write(tmp_file.read())

    print(sample_count, data_size)


if __name__ == "__main__":
    main()
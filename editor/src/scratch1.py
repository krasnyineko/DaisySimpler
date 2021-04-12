from dataclasses import dataclass, field, astuple
from pathlib import Path
import wave
import audioop
import struct

test_path = Path(
    "C:\\Users\\cc4125\source\\repos\\DaisyExamples\\pod\\wavslav\\tools\samples"
)


@dataclass(frozen=True)
class WavInfo:
    path: Path
    frames: int


samples: list[WavInfo] = []
size_bytes = 0
for path in test_path.iterdir():
    if path.is_file == False or path.suffix.lower() != ".wav":
        continue

    with wave.open(str(path), "rb") as wp:
        frames = wp.getnframes()
        wav_info = WavInfo(path, frames)
        size_bytes += frames * 2
        samples.append(wav_info)
        print(wav_info)
        wp.close()

offset = 0
with open(test_path.joinpath("bank"), "wb") as fp:
    fp.write(struct.pack("II", len(samples), size_bytes))
    for sample in samples:
        fp.write(struct.pack("II", offset, sample.frames))
        offset += sample.frames

    for sample in samples:
        with wave.open(str(sample.path), "rb") as wp:
            data = wp.readframes(sample.frames)
            data = audioop.tomono(data, 2, 0.5, 0.5)
            fp.write(data)

print(samples)
# with open(test_path.joinpath("bank"), "wb") as fp:
#     fp.write(struct.pack("B", 3))
#     offset = 0
#     for path in test_path.iterdir():
#         if path.is_file == False or path.suffix.lower() != ".wav":
#             continue

# with wave.open(str(path), "rb") as wav_sample:
#     print(
#         len(
#             audioop.tomono(
#                 wav_sample.readframes(wav_sample.getnframes()), 2, 0.5, 0.5
#             )
#         )
#     )

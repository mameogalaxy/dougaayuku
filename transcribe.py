#!/usr/bin/env python3
"""faster-whisperで日本語文字起こしし、タイムスタンプ付きSRTを出力する。

準備:
    pip install faster-whisper

使い方:
    python transcribe.py 音声または動画ファイル [--model large-v3|medium|small]

入力ファイルと同じ場所に .srt が保存される。
"""
import argparse
import os
import sys
import time


def srt_time(t: float) -> str:
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="日本語文字起こし → SRT(faster-whisper)")
    parser.add_argument("input", help="音声または動画ファイル(.m4a / .mp4 / .mov など)")
    parser.add_argument("--model", default="large-v3", choices=["large-v3", "medium", "small"],
                        help="モデルサイズ(既定: large-v3)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"ファイルが見つかりません: {args.input}")

    try:
        import ctranslate2
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisperが必要です: pip install faster-whisper")

    device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"モデル {args.model} を読み込み中({device})…")
    model = WhisperModel(args.model, device=device, compute_type=compute_type)

    print("文字起こしを開始します…")
    start = time.time()
    segments, info = model.transcribe(args.input, language="ja", vad_filter=True)

    blocks = []
    for i, seg in enumerate(segments, 1):
        text = seg.text.strip()
        blocks.append(f"{i}\n{srt_time(seg.start)} --> {srt_time(seg.end)}\n{text}\n")
        print(f"[{srt_time(seg.start)} → {srt_time(seg.end)}] {text}")

    srt_path = os.path.splitext(args.input)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))
    print(f"\n完了({time.time() - start:.0f}秒) → {srt_path}")


if __name__ == "__main__":
    main()

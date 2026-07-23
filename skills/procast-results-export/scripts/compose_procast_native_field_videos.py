import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


DEFAULT_FFMPEG = Path(os.environ.get("PROCAST_FFMPEG") or shutil.which("ffmpeg") or "ffmpeg")
STEP_RE = re.compile(r"_step(\d+)\.png$", re.IGNORECASE)
VIEW_LABELS = {
    "oblique": "Oblique",
    "pos_z": "+Z looking toward -Z",
    "neg_z": "-Z looking toward +Z",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add a non-overlapping title band to native ProCAST frames and encode MP4 videos."
    )
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--time-csv", type=Path, required=True)
    parser.add_argument("--field", default="temperature")
    parser.add_argument("--field-title", default="Wax Temperature")
    parser.add_argument("--range-label", default="20\u2013170 \u00b0C")
    parser.add_argument("--views", default="oblique,pos_z,neg_z")
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--ffmpeg", type=Path, default=DEFAULT_FFMPEG)
    return parser.parse_args()


def load_step_times(path):
    times = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        columns = raw_line.split()
        if len(columns) < 3:
            continue
        try:
            step = int(columns[0])
            value = float(columns[2])
        except ValueError:
            continue
        times[step] = value
    return times


def load_font(size, bold=False):
    windows_font_dir = Path(os.environ.get("WINDIR", "")) / "Fonts"
    candidates = [
        Path(os.environ.get("PROCAST_FONT_BOLD" if bold else "PROCAST_FONT_REGULAR", "")),
        windows_font_dir / ("segoeuib.ttf" if bold else "segoeui.ttf"),
        windows_font_dir / ("arialbd.ttf" if bold else "arial.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def collect_frames(input_dir, field, view):
    files = []
    pattern = "native_%s_%s_step*.png" % (field.lower().replace(" ", "_"), view)
    for path in input_dir.glob(pattern):
        match = STEP_RE.search(path.name)
        if match:
            files.append((int(match.group(1)), path))
    return sorted(files)


def compose_frame(source, destination, field_title, range_label, view, step, time_value):
    with Image.open(source) as raw:
        raw = raw.convert("RGB")
        canvas = Image.new("RGB", (raw.width, raw.height + 80), "white")
        canvas.paste(raw, (0, 80))
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(28, bold=True)
    subtitle_font = load_font(17, bold=False)
    view_label = VIEW_LABELS.get(view, view)
    time_text = "n/a" if time_value is None else "%.3g s" % time_value
    title = "ProCAST Native | %s | Step %04d | t = %s" % (
        field_title,
        step,
        time_text,
    )
    subtitle = "Fixed range %s | View: %s | Captured every 10 solver steps" % (
        range_label,
        view_label,
    )
    draw.text((28, 8), title, fill=(24, 24, 24), font=title_font)
    draw.text((29, 47), subtitle, fill=(72, 72, 72), font=subtitle_font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="PNG", optimize=True)


def encode_video(ffmpeg, frame_dir, output_path, fps):
    executable = ffmpeg if ffmpeg.exists() else Path(shutil.which("ffmpeg") or "")
    if not executable or not executable.exists():
        raise RuntimeError("ffmpeg executable not found")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(executable),
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frame_dir / "frame_%04d.png"),
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError("ffmpeg failed:\n%s" % completed.stderr[-4000:])
    return command


def main():
    args = parse_args()
    views = [item.strip() for item in args.views.split(",") if item.strip()]
    step_times = load_step_times(args.time_csv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "procast_native_video_composition_v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_dir": str(args.input_dir.resolve()),
        "output_dir": str(args.output_dir.resolve()),
        "time_csv": str(args.time_csv.resolve()),
        "field": args.field,
        "field_title": args.field_title,
        "range_label": args.range_label,
        "fps": args.fps,
        "views": {},
    }

    for view in views:
        native_frames = collect_frames(args.input_dir, args.field, view)
        if not native_frames:
            raise RuntimeError("No native frames found for view %s" % view)
        frame_dir = args.output_dir / ("frames_%s" % view)
        outputs = []
        for index, (step, source) in enumerate(native_frames):
            destination = frame_dir / ("frame_%04d.png" % index)
            compose_frame(
                source,
                destination,
                args.field_title,
                args.range_label,
                view,
                step,
                step_times.get(step),
            )
            outputs.append(
                {
                    "index": index,
                    "step": step,
                    "time_s": step_times.get(step),
                    "source": str(source.resolve()),
                    "frame": str(destination.resolve()),
                }
            )
        video_path = args.output_dir / ("procast_native_%s_%s_every10.mp4" % (args.field, view))
        command = encode_video(args.ffmpeg, frame_dir, video_path, args.fps)
        manifest["views"][view] = {
            "frame_count": len(outputs),
            "first_step": outputs[0]["step"],
            "last_step": outputs[-1]["step"],
            "frames": outputs,
            "video": str(video_path.resolve()),
            "video_bytes": video_path.stat().st_size,
            "ffmpeg_command": command,
        }
        (args.output_dir / "video_composition_manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )

    print(json.dumps({"status": "complete", "views": views}, indent=2))


if __name__ == "__main__":
    main()

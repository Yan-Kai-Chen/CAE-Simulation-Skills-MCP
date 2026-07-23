import json
import os
import sys
import time
import traceback
from pathlib import Path


INPUT_UNF = os.environ.get("PROCAST_INPUT_UNF", "")
OUT_DIR = Path(os.environ.get("PROCAST_NATIVE_OUT_DIR", "."))
FIELD = os.environ.get("PROCAST_NATIVE_FIELD", "Temperature")
UNIT = os.environ.get("PROCAST_NATIVE_UNIT", "C")
STEPS_TEXT = os.environ.get("PROCAST_NATIVE_STEPS", "0,290,770")
VIEWS_TEXT = os.environ.get("PROCAST_NATIVE_VIEWS", "oblique,pos_z,neg_z")
CLIM_MIN = float(os.environ.get("PROCAST_NATIVE_CLIM_MIN", "20"))
CLIM_MAX = float(os.environ.get("PROCAST_NATIVE_CLIM_MAX", "170"))
IMAGE_WIDTH = int(os.environ.get("PROCAST_NATIVE_IMAGE_WIDTH", "1600"))
IMAGE_HEIGHT = int(os.environ.get("PROCAST_NATIVE_IMAGE_HEIGHT", "1000"))
PART_MODE = os.environ.get("PROCAST_NATIVE_PART_MODE", "alloy").strip().lower()
COLOR_LEVELS = int(os.environ.get("PROCAST_NATIVE_COLOR_LEVELS", "8"))
ANIMATION_INCREMENT = int(os.environ.get("PROCAST_NATIVE_ANIMATION_INCREMENT", "10"))
ANIMATION_END = int(os.environ.get("PROCAST_NATIVE_ANIMATION_END", "770"))
VE_COMMON_RESOURCES = os.environ.get("PROCAST_VE_COMMON_RESOURCES", "")
REPORT_PATH = OUT_DIR / "native_field_image_export_manifest.json"


PALETTE_ANCHORS = [
    (33, 102, 172),
    (67, 147, 195),
    (146, 197, 222),
    (209, 229, 240),
    (253, 219, 199),
    (244, 165, 130),
    (214, 96, 77),
    (178, 24, 43),
]

VIEW_VECTORS = {
    "oblique": ((-1.0, -0.82, -0.72), (0.0, 0.0, 1.0)),
    "pos_z": ((0.0, 0.0, -1.0), (0.0, 1.0, 0.0)),
    "neg_z": ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
    "pos_x": ((-1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
    "neg_x": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
}


def add_ve_paths():
    for extra_path in [
        os.path.join(VE_COMMON_RESOURCES, "VPy"),
        os.path.join(VE_COMMON_RESOURCES, "VPy", "Cast"),
        os.path.join(VE_COMMON_RESOURCES, "VisualEnvironment"),
        os.path.join(VE_COMMON_RESOURCES, "VisualCast"),
    ]:
        if extra_path not in sys.path:
            sys.path.insert(0, extra_path)


def parse_ints(text):
    values = []
    for token in text.replace(";", ",").split(","):
        token = token.strip()
        if token:
            values.append(int(token))
    return list(dict.fromkeys(values))


def parse_names(text):
    return [token.strip().lower() for token in text.replace(";", ",").split(",") if token.strip()]


def interpolate_palette(anchors, levels):
    if levels < 2:
        raise ValueError("COLOR_LEVELS must be at least 2")
    colors = []
    segment_count = len(anchors) - 1
    for index in range(levels):
        position = index * segment_count / float(levels - 1)
        left = min(int(position), segment_count - 1)
        fraction = position - left
        right = left + 1
        colors.append(
            tuple(
                int(round(anchors[left][channel] * (1.0 - fraction) + anchors[right][channel] * fraction))
                for channel in range(3)
            )
        )
    return colors


def record(report, stage, status, detail=None):
    report["events"].append(
        {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stage": stage,
            "status": status,
            "detail": detail,
        }
    )


def attempt(report, stage, function, required=True):
    try:
        result = function()
        record(report, stage, "ok", str(result))
        write_report(report)
        return result
    except Exception:
        detail = traceback.format_exc()
        record(report, stage, "error", detail)
        write_report(report)
        if required:
            raise
        return None


def write_report(report):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)


def configure_spectrum(VCmd):
    palette = interpolate_palette(PALETTE_ANCHORS, COLOR_LEVELS)
    command = VCmd.Activate(0, r"VToolKit.VtkScaleControlInterface", r"Spectrum Control")
    VCmd.SetIntValue(command, "SpectrumEnableEdit", 1)
    VCmd.SetStringValue(command, "SpectrumDispMode", "Smeared")
    VCmd.SetIntValue(command, "SpectrumRangeType", 1)
    VCmd.SetDoubleValue(command, "RangeMin", CLIM_MIN)
    VCmd.SetDoubleValue(command, "RangeMax", CLIM_MAX)
    VCmd.SetIntValue(command, "Levels", len(palette))
    for index in range(len(palette) + 1):
        value = CLIM_MIN + (CLIM_MAX - CLIM_MIN) * index / float(len(palette))
        VCmd.SetStringValue(command, "SetCellValue", "%d %.9g" % (index, value))
    for index, rgb in enumerate(palette):
        VCmd.SetStringValue(
            command,
            "SetCellRGB",
            "%d %d %d %d" % (index, rgb[0], rgb[1], rgb[2]),
        )
    VCmd.SetStringValue(command, "SetSpectrumZoneOnOff", "OFF")
    VCmd.SetStringValue(command, "OutOfBoundOnOff", "OFF")
    VCmd.SetStringValue(command, "SpectrumFormat", "2 1")
    VCmd.SetGuStringValue(command, "Orient", "Right")
    VCmd.SetIntValue(command, "ScaleFlipVal", 0)
    VCmd.Accept(command)
    VCmd.Quit(command)


def set_spectrum_minmax_for_current_model(VCmd, VistaDb):
    """Apply a fixed spectrum range using VE18's own simplified-command pattern."""
    current_model = VistaDb.GetCurrentResultModel()
    if current_model is None:
        raise RuntimeError("No current result model is available for spectrum scaling")
    command = VCmd.Activate(
        1,
        r"VToolKit.VtkScaleControlInterface",
        r"Spectrum Control",
    )
    VCmd.SetObjectValue(command, "Model", current_model)
    VCmd.SetPoint2Value(
        command,
        "RangeMinMax",
        "%.9g %.9g" % (CLIM_MIN, CLIM_MAX),
    )
    VCmd.Cancel(command)
    VCmd.Quit(command)


def get_first_window(Viewer, VE):
    page_count, pages = Viewer.GetAllPages()
    for page in list(pages)[:page_count]:
        window_count, windows = VE.GetAllWindows(page)
        if window_count:
            window = VE.GetWindowStr(list(windows)[0])
            page_number = int(window.split("w", 1)[0].lstrip("p"))
            return page_number, window
    raise RuntimeError("No active Viewer page/window was found")


def initialize_animation(ViewerCast, end_step):
    ViewerCast.animtype(1)
    ViewerCast.animstepincrement(ANIMATION_INCREMENT)
    ViewerCast.animstepstart(0)
    ViewerCast.animstepend(end_step)
    ViewerCast.animbgn()


def advance_animation(ViewerCast, current_step, target_step):
    if target_step < current_step:
        raise ValueError("Steps must be in ascending order")
    delta = target_step - current_step
    if delta % ANIMATION_INCREMENT:
        raise ValueError(
            "Step %d is not reachable from %d with animation increment %d"
            % (target_step, current_step, ANIMATION_INCREMENT)
        )
    advances = delta // ANIMATION_INCREMENT
    for _ in range(advances):
        ViewerCast.animnxt()
    return advances


def set_view(VHostManager, VCmd, VgPoint3, view):
    if view not in VIEW_VECTORS:
        raise ValueError("Unsupported view: %s" % view)
    direction, up = VIEW_VECTORS[view]
    VHostManager.SetViewParam(
        VgPoint3(0.0, 0.0, 0.0),
        VgPoint3(up[0], up[1], up[2]),
        VgPoint3(direction[0], direction[1], direction[2]),
        VgPoint3(),
        VgPoint3(),
    )
    fit = VCmd.Activate(1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand")
    VCmd.ExecuteCommand(fit, "Fit")
    VCmd.Quit(fit)


def export_image(VE, VHostManager, page, window, output_path):
    VE.SetActiveWindow(window)
    VE.SetCurrentPage(page)
    VE.Command(">>> showonly(p%s,'%s')" % (page, window.split("w")[-1]))
    VHostManager.Command(">>> pagemodeltitledisp(0)")
    VHostManager.Command(">>> pagewinmarkdisp(0)")
    VE.Command(">>> setpreviewfitstate(1, 0)")
    VE.Command(">>> setheaderfooterflag(0)")
    VHostManager.Command(">>> setmarginflag(0)")
    VHostManager.Command(">>> setimagesize(%d,%d)" % (IMAGE_WIDTH, IMAGE_HEIGHT))
    image_name = str(output_path).replace("\\", "/")
    VE.Command('>>> exportcurrentpagetoimage("%s", "png", 1, 1)' % image_name)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    add_ve_paths()
    steps = parse_ints(STEPS_TEXT)
    views = parse_names(VIEWS_TEXT)
    report = {
        "schema": "procast_native_field_image_export_v1",
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "input_unf": INPUT_UNF,
        "input_exists": os.path.exists(INPUT_UNF),
        "out_dir": str(OUT_DIR),
        "field": FIELD,
        "unit": UNIT,
        "steps": steps,
        "views": views,
        "clim": [CLIM_MIN, CLIM_MAX],
        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
        "part_mode": PART_MODE,
        "palette_anchor_rgb": PALETTE_ANCHORS,
        "color_levels": COLOR_LEVELS,
        "animation_increment": ANIMATION_INCREMENT,
        "animation_end": ANIMATION_END,
        "python": sys.version,
        "events": [],
        "outputs": [],
    }
    write_report(report)

    import VE
    import VCmd
    import VHostManager
    import VistaDb
    import Viewer
    import ViewerCast
    from VgPoint3 import VgPoint3

    try:
        attempt(report, "change_context", lambda: VHostManager.ChangeContext("Visual-Viewer Cast"))
        attempt(report, "set_configuration", lambda: Viewer.SetCurrentConfiguration(2))
        attempt(report, "delete_all", lambda: Viewer.Command(">>> deleteall()"))
        attempt(report, "load_file", lambda: ViewerCast.loadfile(INPUT_UNF))
        time.sleep(2.0)
        attempt(report, "set_unit", lambda: ViewerCast.setunit(FIELD, UNIT))
        attempt(report, "contour", lambda: ViewerCast.contour(FIELD))
        time.sleep(1.0)
        if PART_MODE == "alloy":
            attempt(report, "show_alloy_parts", lambda: ViewerCast.showalloyparts(), required=False)
        elif PART_MODE == "mold":
            attempt(report, "show_mold_parts", lambda: ViewerCast.showmoldparts(), required=False)
        attempt(report, "mesh_smooth", lambda: ViewerCast.setmeshsmooth(1), required=False)
        attempt(report, "hide_model_coordinate_system", lambda: ViewerCast.modelcoordsysstate("off"), required=False)
        page, window = attempt(report, "find_window", lambda: get_first_window(Viewer, VE))
        if steps and max(steps) > ANIMATION_END:
            raise ValueError("Requested step exceeds PROCAST_NATIVE_ANIMATION_END")
        attempt(report, "initialize_animation", lambda: initialize_animation(ViewerCast, ANIMATION_END))
        current_step = 0

        for step in steps:
            advances = attempt(
                report,
                "advance_to_step_%04d" % step,
                lambda step=step, current_step=current_step: advance_animation(
                    ViewerCast, current_step, step
                ),
            )
            current_step = step
            time.sleep(1.0)
            attempt(
                report,
                "fixed_spectrum_step_%04d" % step,
                lambda: set_spectrum_minmax_for_current_model(VCmd, VistaDb),
            )
            # The fixed-range command restores VE's default colors. Reapply the
            # approved palette afterwards; Smeared mode interpolates the anchors.
            attempt(
                report,
                "custom_spectrum_step_%04d" % step,
                lambda: configure_spectrum(VCmd),
            )
            time.sleep(0.5)
            record(report, "display_step_%04d" % step, "ok", {"animation_advances": advances})
            write_report(report)
            for view in views:
                attempt(
                    report,
                    "view_%s_step_%04d" % (view, step),
                    lambda view=view: set_view(VHostManager, VCmd, VgPoint3, view),
                )
                time.sleep(0.5)
                output_path = OUT_DIR / ("native_%s_%s_step%04d.png" % (FIELD.lower().replace(" ", "_"), view, step))
                attempt(
                    report,
                    "export_%s_step_%04d" % (view, step),
                    lambda output_path=output_path: export_image(
                        VE, VHostManager, page, window, output_path
                    ),
                )
                time.sleep(0.5)
                info = {
                    "path": str(output_path),
                    "exists": output_path.exists(),
                    "bytes": output_path.stat().st_size if output_path.exists() else 0,
                    "step": step,
                    "view": view,
                }
                report["outputs"].append(info)
                write_report(report)
    except Exception:
        report["fatal_error"] = traceback.format_exc()
        raise
    finally:
        report["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        write_report(report)
        print("WROTE_REPORT=%s" % REPORT_PATH)


if __name__ == "__main__":
    main()

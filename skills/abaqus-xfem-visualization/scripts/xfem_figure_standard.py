#!/usr/bin/env python3
"""Hard layout and export rules for project XFEM fracture figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BLUE = "#2166AC"
LIGHT_BLUE = "#92C5DE"
PALE_BLUE = "#D1E5F0"
MIST_BLUE = "#B7D9EA"
PALE_RED = "#FDDBC7"
CORAL = "#F4A582"
MID_RED = "#D6604D"
RED = "#B2182B"
MUTED = "#5F6B76"
STANDARD_DPI = 450
DETAIL_DPI = 500
STATUS_TICKS = [0.0, 0.4, 0.7, 1.0]


def add_status_colorbar(fig, norm, cmap, rect, detailed=False):
    """Add STATUSXFEM to a dedicated horizontal band outside plot axes."""
    cax = fig.add_axes(rect)
    colorbar = fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=cax,
        orientation="horizontal",
    )
    label = "STATUSXFEM"
    if detailed:
        label += "  —  0 intact · 0–1 partially cracked · 1 fully cracked"
    colorbar.set_label(label, color=MUTED, fontsize=9.2, labelpad=6)
    colorbar.ax.xaxis.set_label_position("top")
    colorbar.set_ticks(STATUS_TICKS)
    colorbar.ax.tick_params(
        axis="x", labelsize=8.5, labelcolor=MUTED,
        color=MUTED, width=0.65, length=3.0, pad=2,
    )
    colorbar.outline.set_edgecolor(MUTED)
    colorbar.outline.set_linewidth(0.65)
    return cax


def _bbox_overlap(first, second, pad_px=4.0):
    return not (
        first.x1 + pad_px <= second.x0
        or second.x1 + pad_px <= first.x0
        or first.y1 + pad_px <= second.y0
        or second.y1 + pad_px <= first.y0
    )


def assert_colorbar_clear(fig, cbar_ax, plot_axes, protected_artists, figure_name):
    """Fail when a colorbar touches plots, text, notes, or the page edge."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    cbar_box = cbar_ax.get_tightbbox(renderer)
    page_box = fig.bbox
    edge_gap = 4.0
    if (
        cbar_box.x0 < page_box.x0 + edge_gap
        or cbar_box.y0 < page_box.y0 + edge_gap
        or cbar_box.x1 > page_box.x1 - edge_gap
        or cbar_box.y1 > page_box.y1 - edge_gap
    ):
        raise RuntimeError(f"{figure_name}: colorbar crosses the page safe area")
    for index, ax in enumerate(np.ravel(plot_axes)):
        if _bbox_overlap(cbar_box, ax.get_tightbbox(renderer)):
            raise RuntimeError(f"{figure_name}: colorbar overlaps plot axis {index + 1}")
    for name, artist in protected_artists:
        if artist is not None and _bbox_overlap(
            cbar_box, artist.get_window_extent(renderer)
        ):
            raise RuntimeError(f"{figure_name}: colorbar overlaps {name}")


def save_checked_figure(
    fig, png_path, cbar_ax, plot_axes, protected_artists, dpi=STANDARD_DPI
):
    """Validate layout, then save high-DPI PNG and matching PDF."""
    png_path = Path(png_path)
    assert_colorbar_clear(
        fig, cbar_ax, plot_axes, protected_artists, png_path.name
    )
    fig.savefig(png_path, dpi=dpi, facecolor="white")
    fig.savefig(png_path.with_suffix(".pdf"), dpi=dpi, facecolor="white")

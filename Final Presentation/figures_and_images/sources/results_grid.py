"""Grid shared by the Results plots, matching native Figure 5.7."""

TEX_POINT = 72 / 72.27
THESIS_WIDTH_IN = 160 / 25.4


def apply_results_grid(ax, scale=None):
    """Light solid horizontal lines and darker densely dotted vertical lines.

    The default compensates for inclusion at the thesis's 160 mm text width.
    A native presentation panel can pass scale=1 to use the same line styles
    at its own physical size. Tick locations and data limits are retained.
    """
    if scale is None:
        scale = ax.figure.get_figwidth() / THESIS_WIDTH_IN
    ax.set_axisbelow(True)
    ax.grid(False, which="both", axis="both")
    ax.grid(True, which="major", axis="y", color="0.875", alpha=1,
            linewidth=0.2 * TEX_POINT * scale, linestyle="-")
    # pgfplots densely dotted: one line-width on, 1 TeX pt off.
    ax.grid(True, which="major", axis="x", color="0.675", alpha=1,
            linewidth=0.4 * TEX_POINT * scale,
            linestyle=(0, (1, 2.5)), dash_capstyle="butt")

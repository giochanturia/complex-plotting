import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.colors as colors
from matplotlib import cm

# Plotting parameters for the notebook:
plt.rcParams["figure.figsize"] = [8, 4]
plt.rcParams["figure.dpi"] = 100

plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})
plt.rc("text", usetex=True)

n_mesh = 120
x_range = 1.0
y_range = 1.0
y_near_zero = 0.01
z_re = np.linspace(-x_range, x_range, n_mesh)
z_im = np.concatenate(
    (
        np.linspace(-y_range, -y_near_zero, n_mesh // 2),
        np.array([0]),
        np.linspace(y_near_zero, y_range, n_mesh // 2),
    )
)
z_RE, z_IM = np.meshgrid(z_re, z_im)
z_CP = z_RE + 1j * z_IM


def extra_curve(z_re, z_im, quantity, color="red", linestyle="solid"):
    return {"re": z_re, "im": z_im, "q": quantity, "c": color, "ls": linestyle}


def plot_complex(
    z_RE,
    z_IM,
    quantity,
    label,
    plot_type="contourf",
    axislines=[[(0,0), {'c': 'k', 'alpha': 0.25}]],
    halfrange=None,
    plotrange=None,
    extra_curves=[],
    xticks=None,
    yticks=None,
):
    quantity = np.array(quantity).astype(np.complex64)
    extra_params = {}
    extra_params_centered = {}
    if halfrange is not None:
        extra_params = {"vmax": 2 * halfrange}
        extra_params_centered = {"halfrange": halfrange}

    fig = plt.figure(figsize=(10, 6))

    ax_re = fig.add_subplot(2, 3, 1)
    ax_im = fig.add_subplot(2, 3, 2)
    ax_abs = fig.add_subplot(2, 3, 3)
    ax_re_3d = fig.add_subplot(2, 3, 4, projection="3d", computed_zorder=False)
    ax_im_3d = fig.add_subplot(2, 3, 5, projection="3d", computed_zorder=False)
    ax_abs_3d = fig.add_subplot(2, 3, 6, projection="3d", computed_zorder=False)

    # Surface plots:
    if plot_type == "contourf":
        cf_re = ax_re.contourf(
            z_RE,
            z_IM,
            np.real(quantity),
            levels=32,
            cmap="RdYlGn",
            norm=colors.CenteredNorm(**extra_params_centered),
        )
        cf_im = ax_im.contourf(
            z_RE,
            z_IM,
            np.imag(quantity),
            levels=32,
            cmap="RdYlGn",
            norm=colors.CenteredNorm(**extra_params_centered),
        )
        cf_abs = ax_abs.contourf(
            z_RE,
            z_IM,
            np.abs(quantity),
            levels=32,
            cmap="Blues",
            norm=colors.Normalize(**extra_params),
        )
    else:
        cf_re = ax_re.pcolormesh(
            z_RE,
            z_IM,
            np.real(quantity),
            cmap="RdYlGn",
            norm=colors.CenteredNorm(**extra_params_centered),
        )
        cf_im = ax_im.pcolormesh(
            z_RE,
            z_IM,
            np.imag(quantity),
            cmap="RdYlGn",
            norm=colors.CenteredNorm(**extra_params_centered),
        )
        cf_abs = ax_abs.pcolormesh(
            z_RE,
            z_IM,
            np.abs(quantity),
            cmap="Blues",
            norm=colors.Normalize(**extra_params),
        )

    ax_re.set_title(rf"Re ${label}$")
    ax_im.set_title(rf"Im ${label}$")
    ax_abs.set_title(rf"$|{label}|$")

    # 3D plots:
    ax_re_3d.plot_surface(
        z_RE,
        z_IM,
        np.real(quantity),
        cmap="RdYlGn",
        norm=colors.CenteredNorm(**extra_params_centered),
        alpha=0.9,
        zorder=1,
    )
    ax_im_3d.plot_surface(
        z_RE,
        z_IM,
        np.imag(quantity),
        cmap="RdYlGn",
        norm=colors.CenteredNorm(**extra_params_centered),
        alpha=0.9,
        zorder=1,
    )
    ax_abs_3d.plot_surface(
        z_RE,
        z_IM,
        np.abs(quantity),
        cmap="Blues",
        norm=colors.Normalize(**extra_params),
        alpha=0.9,
        zorder=1,
    )

    for e in extra_curves:
        ax_re_3d.plot(e["re"], e["im"], np.real(e["q"]), c=e["c"], ls=e["ls"], zorder=2)
        ax_im_3d.plot(e["re"], e["im"], np.imag(e["q"]), c=e["c"], ls=e["ls"], zorder=2)
        ax_abs_3d.plot(e["re"], e["im"], np.abs(e["q"]), c=e["c"], ls=e["ls"], zorder=2)

    for ax in [ax_re, ax_im, ax_abs]:
        if axislines:
            for p in axislines:
                ax.axvline(p[0][0], **p[1])
                ax.axhline(p[0][1], **p[1])
        ax.set_aspect("equal")

    if plotrange is not None:
        ax_re_3d.set_zlim((-plotrange, plotrange))
        ax_im_3d.set_zlim((-plotrange, plotrange))
        ax_abs_3d.set_zlim((0, 2 * plotrange))

    for ax in [ax_re, ax_im, ax_abs, ax_re_3d, ax_im_3d, ax_abs_3d]:
        if xticks is not None:
            ax.set_xticks(*xticks)
        if yticks is not None:
            ax.set_yticks(*yticks)

    fig.colorbar(cf_re, ax=ax_re)
    fig.colorbar(cf_im, ax=ax_im)
    fig.colorbar(cf_abs, ax=ax_abs)

    plt.tight_layout()
    return fig
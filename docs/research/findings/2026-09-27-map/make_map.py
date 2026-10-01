"""SR-177 Weber County route options map (research exhibit, 2026-09-27).

Inputs are JSON pulls (Esri JSON, WGS84) from public services, saved in this folder:
  UGRC: roads, munis, counties, streams, lakes, rail, power
  WFRC: wfrc_wwc (2023-2050 RTP roadway project lines, OBJECTID 52,53,54,101,102)
  HDR public ArcGIS items: hdr_study, hdr_wma, hdr_lwcf
"""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, FancyBboxPatch
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.patheffects as pe
import shapely
from shapely.geometry import Polygon, LineString, Point

OUT = sys.argv[1] if len(sys.argv) > 1 else "sr177_route_options"
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 240

# ---------- projection: local equirectangular in km ----------
LAT0, LON0 = 41.24, -112.10
KX = 111.320 * np.cos(np.radians(LAT0))
KY = 110.95
def P(lon, lat):
    return (np.asarray(lon) - LON0) * KX, (np.asarray(lat) - LAT0) * KY

EXT = (-112.232, -111.968, 41.098, 41.382)   # lon min, lon max, lat min, lat max
x0, y0 = P(EXT[0], EXT[2]); x1, y1 = P(EXT[1], EXT[3])

# ---------- palette (dataviz reference palette, light mode) ----------
SURF = "#f4f3ef"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8984"
BLUE, BLUE_CASING = "#2a78d6", "#b7d3f6"      # series-1, sequential 150
ORANGE = "#eb6834"                              # series-2
VIOLET = "#4a3aa7"                              # series-3 (validated all-pairs w/ 1,2)
HIST = "#5f5e59"                                # neutral: historical options
WATER, WATER_LINE = "#d3e3f0", "#6f9fc8"
WMA_FILL, WMA_EDGE, WMA_TEXT = "#dfead7", "#8fae80", "#4d6b43"
halo = [pe.withStroke(linewidth=4, foreground="white")]
halo_s = [pe.withStroke(linewidth=3, foreground=SURF)]

def load(n):
    return json.load(open(n + ".json"))["features"]

def paths_of(f):
    return [np.array(pa) for pa in f["geometry"].get("paths", [])]

def rings_path(rings):
    verts, codes = [], []
    for r in rings:
        r = np.array(r)
        xs, ys = P(r[:, 0], r[:, 1])
        verts += list(zip(xs, ys)); codes += [Path.MOVETO] + [Path.LINETO] * (len(r) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes)

def rings_to_poly(rings):
    return shapely.unary_union([Polygon(r).buffer(0) for r in rings])

# ---------- data ----------
counties = {f["attributes"]["NAME"]: f for f in load("counties")}
weber = rings_to_poly(counties["WEBER"]["geometry"]["rings"])
roads = load("roads")
wfrc = {f["attributes"]["OBJECTID"]: f for f in json.load(open("wfrc_wwc.json"))["features"]}

def street_pos(name, idx):
    vals = []
    for f in roads:
        if f["attributes"]["FULLNAME"] == name:
            for pts in paths_of(f):
                m = shapely.contains_xy(weber, pts[:, 0], pts[:, 1])
                vals += list(pts[m][:, idx])
    return float(np.median(vals))

# Weber County grid: address -> coordinate (interpolated from UGRC centerlines)
NS = {w: street_pos(f"{w} W", 0) for w in [1900, 3500, 4700, 5100, 5900, 6300, 6700, 7500, 8300]}
EW = {-5500: street_pos("5500 S", 1), -4000: street_pos("4000 S", 1), -3300: street_pos("3300 S", 1),
      -2550: street_pos("2550 S", 1), -1800: street_pos("1800 S", 1), -1200: street_pos("12TH ST", 1),
      -900: street_pos("900 S", 1), 900: street_pos("900 N", 1), 1800: street_pos("1800 N", 1),
      2700: street_pos("2700 N", 1), 4000: street_pos("4000 N", 1)}
def lon_of(w):
    ks = sorted(NS); return float(np.interp(w, ks, [NS[k] for k in ks]))
def lat_of(a):   # a<0 south
    ks = sorted(EW); return float(np.interp(a, ks, [EW[k] for k in ks]))

def chaikin(pts, it=3):
    pts = np.asarray(pts, float)
    for _ in range(it):
        q = 0.75 * pts[:-1] + 0.25 * pts[1:]; r = 0.25 * pts[:-1] + 0.75 * pts[1:]
        new = np.empty((2 * len(q), 2)); new[0::2] = q; new[1::2] = r
        pts = np.vstack([pts[0], new, pts[-1]])
    return pts

# ---------- figure ----------
FW, FH = 31.0, 23.0
fig = plt.figure(figsize=(FW, FH), facecolor="white")
map_h = 21.2 / FH
map_w = map_h * FH / FW * (x1 - x0) / (y1 - y0)
MAP_L = 0.215
ax = fig.add_axes([MAP_L, 0.035, map_w, map_h])
ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal")
ax.set_facecolor(SURF)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color(INK2); s.set_linewidth(1.2)

# water bodies
for f in load("lakes"):
    t = f["attributes"]["FType_Text"]
    col = WATER if t in ("Lake/Pond", "Reservoir") else "#e6eee4"
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor=col, edgecolor="none", zorder=1))

# wildlife management areas: full DWR boundaries, plus portions inside HDR's study buffer (hatched)
plt.rcParams["hatch.color"] = WMA_TEXT
plt.rcParams["hatch.linewidth"] = 0.8
dwr = [f for f in load("dwr_wma") if f["attributes"]["type_"] in ("Wildlife Management Area", "Waterfowl Management Area", "Conservation Easement")
       and (f["attributes"]["acres"] or 0) > 100]
for f in dwr:
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor=WMA_FILL, edgecolor=WMA_EDGE,
                           linewidth=0.9, zorder=1.4, alpha=0.95))
for f in load("hdr_wma"):
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor="#c9dcbf", edgecolor=WMA_TEXT,
                           hatch="///", linewidth=1.0, zorder=1.5))

# municipalities
for f in load("munis"):
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor="#ebe8e0", edgecolor="#b5b1a6",
                           linewidth=0.9, linestyle=(0, (4, 3)), zorder=2, alpha=0.9))

# roads
styles = {"1": ("#4f4e4a", 3.4, 6), "3": ("#6c6a64", 2.0, 5.5), "4": ("#6c6a64", 1.8, 5.5), "5": ("#6c6a64", 1.8, 5.5),
          "6": ("#7b7973", 1.4, 5.4), "7": ("#8e8c86", 0.7, 5.2), "8": ("#9f9d96", 0.95, 5), "10": ("#a7a59e", 0.8, 4.9)}
groups = {}
for f in roads:
    c = f["attributes"]["CARTOCODE"]
    col, lw, z = styles.get(c, ("#d0cec7", 0.35, 4))
    for pts in paths_of(f):
        xs, ys = P(pts[:, 0], pts[:, 1])
        groups.setdefault((col, lw, z), []).append(np.column_stack([xs, ys]))
for (col, lw, z), segs in groups.items():
    ax.add_collection(LineCollection(segs, colors=col, linewidths=lw, zorder=z, capstyle="round"))

# railroads
rsegs = []
for f in load("rail"):
    if f["attributes"].get("RAILROAD") in ("Union Pacific", "Utah Central", "UT Transit Auth"):
        for pts in paths_of(f):
            xs, ys = P(pts[:, 0], pts[:, 1]); rsegs.append(np.column_stack([xs, ys]))
ax.add_collection(LineCollection(rsegs, colors="#6f6d67", linewidths=1.1, linestyles=(0, (5, 2.5)), zorder=5.6))

# transmission lines (>=138 kV)
psegs = []
for f in load("power"):
    if f["attributes"]["LAYER"] in ("KV-138", "KV-230", "KV-345"):
        for pts in paths_of(f):
            xs, ys = P(pts[:, 0], pts[:, 1]); psegs.append(np.column_stack([xs, ys]))
ax.add_collection(LineCollection(psegs, colors="#b3a58a", linewidths=0.8, linestyles=(0, (2, 2)), zorder=5.5))

# Weber River
for f in load("streams"):
    if f["attributes"]["GNIS_Name"] in ("Weber River", "Ogden River"):
        for pts in paths_of(f):
            xs, ys = P(pts[:, 0], pts[:, 1])
            ax.plot(xs, ys, color=WATER_LINE, lw=2.4, zorder=5.7, solid_capstyle="round")

# county lines
for name, f in counties.items():
    for r in f["geometry"]["rings"]:
        r = np.array(r); xs, ys = P(r[:, 0], r[:, 1])
        ax.plot(xs, ys, color="#3d3c39", lw=2.0, ls=(0, (10, 3, 2, 3)), zorder=6)

# ---------- thematic overlays ----------
def wline(oid):
    return np.vstack([np.array(pa) for pa in wfrc[oid]["geometry"]["paths"]])
seg_davis_ses = wline(101)   # Weber Co line -> 1800 N (Davis), RTP phase 2
seg_uc = wline(102)          # 1800 N -> SR-193, phase 1 (under construction)
seg_p2 = wline(54)           # Davis Co line -> 4000 S, RTP phase 2
seg_p3 = wline(53)           # 4000 S -> 12th St/900 S, RTP phase 3
seg_unf = wline(52)          # 900 S -> I-15 north, unfunded (phase code 4)

def orient_north(a):
    return a if a[0, 1] < a[-1, 1] else a[::-1]
seg_davis_ses, seg_p2, seg_p3 = map(orient_north, (seg_davis_ses, seg_p2, seg_p3))

def plot_ll(a, **kw):
    xs, ys = P(a[:, 0], a[:, 1]); return ax.plot(xs, ys, **kw)

# HDR "SR177 Phase 4" study area (working GIS)
hdr = load("hdr_study")[0]
ax.add_patch(PathPatch(rings_path(hdr["geometry"]["rings"]), facecolor=ORANGE, alpha=0.07, edgecolor="none", zorder=6.5))
ax.add_patch(PathPatch(rings_path(hdr["geometry"]["rings"]), facecolor="none", edgecolor=ORANGE, linewidth=3.2,
                       linestyle=(0, (7, 3)), zorder=6.6))

# current UDOT SES segment casing (1800 N West Point -> 4000 S West Haven)
ses = np.vstack([seg_davis_ses, seg_p2])
plot_ll(ses, color=BLUE_CASING, lw=30, zorder=7, solid_capstyle="round", alpha=0.95)

# existing SR-177 + under construction
for f in roads:
    if "WEST DAVIS" in (f["attributes"]["FULLNAME"] or "") and "RAMP" not in f["attributes"]["FULLNAME"]:
        for pts in paths_of(f):
            plot_ll(pts, color="#1f1f1d", lw=5.5, zorder=8, solid_capstyle="round")
plot_ll(seg_uc, color="#1f1f1d", lw=5.5, ls=(0, (2.2, 1.2)), zorder=8)

# historical options (neutral dotted)
# (a) power-line corridor ~3100 W (2007 public favorite; rejected 2009) - actual 345 kV line geometry
for f in load("power"):
    if f["attributes"]["OBJECTID"] == 2067:
        for pts in paths_of(f):
            pts = pts[(pts[:, 1] >= lat_of(-4000)) & (pts[:, 1] <= lat_of(4000))]
            if len(pts) < 2: continue
            plot_ll(pts, color=HIST, lw=4.2, ls=(0, (1, 1.6)), zorder=7.5, dash_capstyle="round")
# (b) WDC EIS preliminary Alt 12A (Weber portion): 6500 W through Hooper to 4600 S, NE to 4000 S at 5900 W (approx.)
cl_lat = seg_p2[0, 1]
a12 = np.array([[lon_of(6500), cl_lat], [lon_of(6500), lat_of(-4600)], [lon_of(5900), lat_of(-4000)]])
plot_ll(chaikin(a12, 2), color=HIST, lw=4.2, ls=(0, (1, 1.6)), zorder=7.5, dash_capstyle="round")

# adopted long-range corridor (WFRC 2023-2050 RTP geometry; matches Weber Co. 2009/2021 preserved corridor)
for seg in (seg_davis_ses, seg_p2, seg_p3):
    plot_ll(seg, color="white", lw=9.5, zorder=8.9, solid_capstyle="round")
    plot_ll(seg, color=BLUE, lw=6.5, zorder=9, solid_capstyle="round")
plot_ll(seg_unf, color="white", lw=9.5, zorder=8.9)
plot_ll(seg_unf, color=BLUE, lw=6.5, ls=(0, (3.2, 1.4)), zorder=9)

# West Warren variant ~6300 W (2009 study / 2021 county map dashed; approx.)
def nearest_on(seg, lat):
    i = int(np.argmin(np.abs(seg[:, 1] - lat))); return seg[i]
line_n = np.vstack([seg_p3, orient_north(seg_unf)])


# 8300 W corridor / freeway loop (Weber Co. general plan; approx. redraw of county map)
loop = np.array([nearest_on(line_n, lat_of(-2300)), [lon_of(7500), lat_of(-2100)], [lon_of(8300), lat_of(-1850)],
                 [lon_of(8300), lat_of(-900)], [lon_of(8300), lat_of(1200)], [lon_of(7900), lat_of(1700)],
                 [lon_of(7100), lat_of(1950)], nearest_on(line_n, lat_of(2050))])
plot_ll(chaikin(loop, 3), color=VIOLET, lw=3.6, ls=(0, (8, 3, 2, 3)), zorder=8.7)

# points: Westbridge Meadows freeway-parcel requirement; LWCF park
wx, wy = P(lon_of(7300), lat_of(-1450))
ax.scatter([wx], [wy], marker="s", s=220, color=VIOLET, edgecolor="white", linewidth=2, zorder=10)
lw_pt = load("hdr_lwcf")[0]["geometry"]
lx, ly = P(lw_pt["x"], lw_pt["y"])
ax.scatter([lx], [ly], marker="o", s=200, color=WMA_TEXT, edgecolor="white", linewidth=2, zorder=10)

# ---------- labels ----------
def T(lon, lat, s, **kw):
    x, y = P(lon, lat); kw.setdefault("zorder", 12); return ax.text(x, y, s, **kw)

# street grid reference labels (Weber County grid)
for w in [1900, 3500, 4700, 5100, 5900, 6700, 7500, 8300]:
    for la in (lat_of(-4450), lat_of(3350)):
        if w == 8300: la = lat_of(-600)
        if w in (1900,) and la > lat_of(0): continue
        if w == 7500 and la > lat_of(0): la = lat_of(2350)
        dx = 0.0028 if w == 8300 else (0.0042 if (w == 5100 and la < lat_of(-4000)) else 0.0009)
    T(lon_of(w) + dx, la, f"{w} W", fontsize=12, color=INK2, rotation=90, ha="left", va="center",
          path_effects=halo_s, zorder=11)
for a, lab in [(-5500, "5500 S"), (-4000, "4000 S"), (-3300, "3300 S"), (-2550, "2550 S"), (-1800, "1800 S"),
               (-1200, "12th St"), (-900, "900 S"), (900, "900 N"), (1800, "1800 N"), (2700, "2700 N"), (4000, "4000 N")]:
    for lo, hal in ((EXT[0] + 0.004, "left"), (EXT[1] - 0.003, "right")):
        if hal == "right" and a > 3000: continue
        T(lo, lat_of(a) + 0.0009, lab, fontsize=12, color=INK2, ha=hal, va="bottom", path_effects=halo_s, zorder=11)

# roads
T(-112.0245, 41.322, "I-15", fontsize=15, weight="bold", color=INK, path_effects=halo, rotation=0)
T(-112.0305, 41.155, "I-15", fontsize=15, weight="bold", color=INK, path_effects=halo)
T(lon_of(4700) - 0.0012, lat_of(-2950), "SR-134 (4700 W)", fontsize=12, color=INK2, rotation=90, ha="right", path_effects=halo_s)
T(-112.086, 41.1115, "SR-193", fontsize=12, color=INK2, path_effects=halo_s)
T(-112.069, 41.1005, "Existing SR-177 (West Davis Hwy)", fontsize=12.5, color=INK, path_effects=halo, ha="left", va="bottom")
T(-112.214, 41.2548, "Union Pacific RR", fontsize=11.5, color=INK2, style="italic", path_effects=halo_s, rotation=0)

# water / land
T(-112.228, 41.36, "Great Salt Lake", fontsize=15, color="#4f7fa8", style="italic", path_effects=halo_s)
T(-112.021, 41.371, "Willard Bay", fontsize=13, color="#4f7fa8", style="italic", path_effects=halo_s)
T(-112.061, 41.2235, "Weber River", fontsize=13, color="#3f6f98", style="italic", path_effects=halo_s, rotation=-28)
T(-112.186, 41.333, "Harold S. Crane WMA", fontsize=13, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)
T(-112.21, 41.216, "Ogden Bay WMA", fontsize=13, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)
T(-112.071, 41.3585, "Willard Bay\nUpland Game Area", fontsize=11.5, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)
T(lw_pt["x"] + 0.0022, lw_pt["y"] - 0.0028, "Plain City Park (LWCF-funded)", fontsize=11.5, color=WMA_TEXT, va="center", path_effects=halo_s)

# cities
for name, lon, lat in [("HOOPER", -112.155, 41.168), ("WEST HAVEN", -112.075, 41.2), ("ROY", -112.043, 41.172),
                       ("WEST POINT", -112.095, 41.128), ("PLAIN CITY", -112.084, 41.3105), ("FARR WEST", -111.997, 41.309),
                       ("MARRIOTT-\nSLATERVILLE", -112.02, 41.268), ("OGDEN", -111.992, 41.232), 
                       ("CLINTON", -112.063, 41.13), ("RIVERDALE", -111.998, 41.18)]:
    T(lon, lat, name, fontsize=15, color="#8a877e", weight="bold", ha="center", va="center", path_effects=halo_s, zorder=3)
for name, lon, lat in [("West Warren", -112.18, 41.296), ("Reese", -112.172, 41.262), ("Taylor", -112.085, 41.225),
                       ("West Weber", -112.083, 41.2595)]:
    T(lon, lat, name, fontsize=12.5, color="#8a877e", style="italic", ha="center", path_effects=halo_s, zorder=3)
T(-112.226, 41.151, "WEBER CO.", fontsize=13, color="#3d3c39", weight="bold", path_effects=halo_s, va="bottom")
T(-112.226, 41.147, "DAVIS CO.", fontsize=13, color="#3d3c39", weight="bold", path_effects=halo_s, va="top")
T(-112.226, 41.3775, "BOX ELDER CO.", fontsize=13, color="#3d3c39", weight="bold", path_effects=halo_s)

# route labels (direct labels = secondary encoding)
def fig_xy(lon, lat):
    x, y = P(lon, lat)
    return MAP_L + map_w * (x - x0) / (x1 - x0), 0.035 + map_h * (y - y0) / (y1 - y0)

def callout_in(lon, lat, tlon, tlat, text, color, fs=12.5):
    ax.annotate(text, xy=P(lon, lat), xytext=P(tlon, tlat), fontsize=fs, color=INK, ha="left", va="center", zorder=13,
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=color, lw=1.8, alpha=0.97),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, shrinkA=2, shrinkB=4, mutation_scale=18))

line_n_pt = lambda lat: nearest_on(line_n, lat)
margin = [  # (target lon, target lat, text, color)
    (-112.1286, 41.3037, "HDR working map: “SR177 Phase 4” study area\n(“SR-177 Level 2 Screening” web map,\nAug 24 – Sep 8 2026). 4000 S north to Willard.\nUnofficial consultant GIS; no route lines shown.", ORANGE),
    (lon_of(8300), lat_of(-300), "8300 W corridor (Weber Co. general plan):\npreserve ≥270 ft for a possible freeway\nloop to/from SR-177 (approx.)", VIOLET),
    (*line_n_pt(lat_of(-1000)), "Weber County Commission, Jun 29 2026:\nletter to UDOT & state officials to keep the\n“West Weber freeway” WEST of the Weber River", BLUE),
    (wx / KX + LON0, wy / KY + LAT0, "Westbridge Meadows (≈1400 S, 7500 W):\n300-ft “West Weber Corridor” freeway parcel\nrequired; exact spot to be set with UDOT", VIOLET),
    (*line_n_pt(lat_of(-2550)), "County planner, Aug 4 2026: the 2009 line near\n2550 S crosses federally funded state land &\nwetlands; staff drew an alternative that curves\naround them (not published)", VIOLET),
    (*line_n_pt(lat_of(-3150)), "Adopted line leaves 5100 W at about\n3000–3300 S, then curves northwest across\nthe Weber River (WFRC 2023–2050 RTP;\nWeber Co. 2009 study & 2021 map)", BLUE),
    (lon_of(6500), lat_of(-5100), "HISTORICAL: West Davis EIS preliminary\nAlt 12A, 6500 W through Hooper (dropped\nby 2017; approx.)", HIST),
    (*seg_davis_ses[len(seg_davis_ses) // 2], "CURRENT UDOT STUDY (State Environmental Study):\n1800 N (West Point) → ~4000 S (West Haven) on\n5100 W. West Haven minutes, Mar 4 2026: UDOT\n“settled on an alignment on 5100 W” with the\nexisting road as a frontage road. Draft study\nexpected fall 2026.", BLUE),
]
FS_M = 13
line_h = FS_M * 1.26 / 72 / FH
placed = []
cursor = 0.975
for tlon, tlat, text, color in sorted(margin, key=lambda m: -m[1]):
    n = text.count("\n") + 1
    h = n * line_h + 0.012
    ty = fig_xy(tlon, tlat)[1]
    cy = min(ty, cursor - h / 2)
    cy = max(cy, h / 2 + 0.01)
    cursor = cy - h / 2 - 0.012
    fig.patches  # noqa
    ax.annotate(text, xy=P(tlon, tlat), xytext=(0.008, cy), textcoords="figure fraction", annotation_clip=False,
                fontsize=FS_M, color=INK, ha="left", va="center", zorder=13, linespacing=1.26,
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=color, lw=1.9),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, shrinkA=2, shrinkB=5, mutation_scale=18,
                                connectionstyle="angle3,angleA=0,angleB=90" if False else "arc3,rad=0"))

callout_in(-112.100, 41.238, -112.058, 41.2455,
           "REPORTED — NO LINE PUBLISHED\nUDOT Region 1 “prefers an eastern\nalignment” north of West Haven\n(Weber Co. joint meeting, Mar 3 2026).\nExact location unknown, so not drawn.", ORANGE, fs=12.5)
callout_in(-112.0555, 41.2895, -112.034, 41.2835,
           "HISTORICAL: power-line corridor\n(~3100 W). 2007 public favorite;\nrejected 2009.", HIST, fs=12.5)

# phase tags along the adopted line
for (lon, lat, s) in [(lon_of(5100) + 0.0012, lat_of(-4700), "RTP Phase 2\n(2033–42)"),
                      (lon_of(5900) - 0.0005, lat_of(-2000), "RTP Phase 3\n(2043–50)"),
                      (lon_of(6700) - 0.0015, lat_of(1500), "RTP:\nunfunded")]:
    T(lon, lat, s, fontsize=11.5, color=BLUE, weight="bold", ha="right" if "unfunded" in s else "left", va="center", path_effects=halo)

# north arrow + scale bar (miles)
nx, ny = P(-111.978, 41.366)
ax.annotate("", xy=(nx, ny + 1.2), xytext=(nx, ny - 0.4), arrowprops=dict(arrowstyle="-|>", lw=2.4, color=INK, mutation_scale=30), zorder=14)
ax.text(nx, ny + 1.35, "N", ha="center", va="bottom", fontsize=18, weight="bold", color=INK, path_effects=halo, zorder=14)
sx, sy = P(-112.228, 41.106)
mi = 1.609344
for i in range(4):
    ax.add_patch(plt.Rectangle((sx + i * mi, sy), mi, 0.18, facecolor=INK if i % 2 == 0 else "white", edgecolor=INK, lw=1, zorder=14))
for i in range(5):
    ax.text(sx + i * mi, sy + 0.32, f"{i}", ha="center", va="bottom", fontsize=12, color=INK, path_effects=halo, zorder=14)
ax.text(sx + 4 * mi + 0.35, sy + 0.1, "miles", va="center", fontsize=12, color=INK, path_effects=halo, zorder=14)

# ---------- side panel ----------
px = MAP_L + map_w + 0.016
pw = 1 - px - 0.015
fig.text(px, 0.965, "SR-177 in Weber County:\nroute options on the record", fontsize=30, weight="bold", color=INK, va="top")
fig.text(px, 0.892, "Adopted corridor, current UDOT study, reported alternatives,\nand historical options — with existing roads. As of Sept 27, 2026.",
         fontsize=14.5, color=INK2, va="top")

handles = [
    (Line2D([0], [0], color="#1f1f1d", lw=5.5), "Existing SR-177 (West Davis Hwy)"),
    (Line2D([0], [0], color="#1f1f1d", lw=5.5, ls=(0, (2.2, 1.2))), "Under construction: SR-193 → 1800 N (2026–29)"),
    (Line2D([0], [0], color=BLUE_CASING, lw=16), "Current UDOT State Environmental Study segment"),
    (Line2D([0], [0], color=BLUE, lw=6), "Adopted long-range corridor, funded RTP phases\n(WFRC 2023–2050 RTP; Weber Co. preserved corridor)"),
    (Line2D([0], [0], color=BLUE, lw=6, ls=(0, (3.2, 1.4))), "Adopted corridor, unfunded in RTP (900 S → I-15)"),
    (Patch(facecolor=(0.92, 0.41, 0.2, 0.08), edgecolor=ORANGE, lw=2.5, ls="--"), "HDR working-map study area “SR177 Phase 4”\n(unofficial consultant GIS, Aug–Sep 2026)"),
    (Line2D([0], [0], color=VIOLET, lw=3.6, ls=(0, (8, 3, 2, 3))), "8300 W freeway-loop corridor (Weber Co. plan), approx."),
    (Line2D([0], [0], marker="s", color="white", markerfacecolor=VIOLET, markersize=13, lw=0), "Westbridge Meadows freeway-parcel requirement"),
    (Line2D([0], [0], color=HIST, lw=4.2, ls=(0, (1, 1.6))), "Historical options, dropped or rejected (approx.)"),
    (Patch(facecolor=WMA_FILL, edgecolor=WMA_EDGE), "State wildlife areas & conservation easements (DWR)"),
    (Patch(facecolor="#c9dcbf", edgecolor=WMA_TEXT, hatch="///"), "…portions inside HDR's study buffer"),
    (Line2D([0], [0], color=WATER_LINE, lw=2.4), "Weber River"),
    (Line2D([0], [0], color="#4f4e4a", lw=3.4), "Interstate"),
    (Line2D([0], [0], color="#6c6a64", lw=1.8), "State / U.S. highways"),
    (Line2D([0], [0], color="#a7a59e", lw=0.9), "Major local roads"),
    (Line2D([0], [0], color="#d0cec7", lw=0.8), "Local roads"),
    (Line2D([0], [0], color="#6f6d67", lw=1.1, ls=(0, (5, 2.5))), "Railroads"),
    (Line2D([0], [0], color="#b3a58a", lw=1.0, ls=(0, (2, 2))), "Transmission lines (138–345 kV)"),
    (Patch(facecolor="#ebe8e0", edgecolor="#b5b1a6", ls="--"), "City limits"),
    (Line2D([0], [0], color="#3d3c39", lw=2.0, ls=(0, (10, 3, 2, 3))), "County line"),
]
lax = fig.add_axes([px, 0.47, pw, 0.40]); lax.axis("off")
lax.legend([h for h, _ in handles], [t for _, t in handles], loc="upper left", frameon=False, fontsize=13.5,
           handlelength=4.2, handleheight=1.3, labelspacing=0.72, borderaxespad=0, title="Legend",
           title_fontproperties={"size": 16, "weight": "bold"}, alignment="left")

events = [
    ("Mar 3", "Weber Co. told UDOT Region 1 prefers an “eastern alignment”\nnorth of West Haven"),
    ("Mar 4", "West Haven told UDOT has “settled on” 5100 W (study segment)"),
    ("Jun 29", "County approves letter: keep the freeway west of the Weber River"),
    ("Aug 4", "County staff show an alternative around state land & wetlands"),
    ("Aug 24–Sep 8", "HDR “SR-177 Level 2 Screening” map, “Phase 4” study area"),
    ("Fall", "Draft State Environmental Study expected (1800 N → 4000 S)"),
]
ey = 0.5
fig.text(px, ey, "Key 2026 events", fontsize=14, weight="bold", color=INK, va="top")
ey -= 0.022
for d, t in events:
    fig.text(px, ey, d, fontsize=13, weight="bold", color=INK2, va="top")
    fig.text(px + 0.062, ey, t, fontsize=13, color=INK2, va="top", linespacing=1.3)
    ey -= 0.0152 * (t.count("\n") + 1) + 0.0045
notes_parts = ['How to read this map\n• South of 4000 S, every current source puts SR-177 on 5100 W.\n• North of 4000 S there is no UDOT-approved line. The blue line is the\n  regional plan / county-preserved corridor. UDOT Region 1 reportedly\n  prefers an “eastern” alignment; Weber County is pushing to keep it\n  west of the Weber River. Neither alternative has been published.\n• “Approx.” lines were redrawn by hand from study text or county maps.\n• In West Warren (≈900 S–900 N) the 2009 study left open an 800-ft\n  shift from ≈6500 W to ≈6300 W; the plan line already runs near 6300 W.', 'Sources\nRoads, city & county limits, NHD rivers/lakes, railroads, transmission\nlines: Utah Geospatial Resource Center (UGRC), retrieved Sep 27 2026.\nAdopted corridor + phases: WFRC 2023–2050 RTP Roadway Projects layer.\nStudy area & buffer-clipped wildlife areas: public HDR ArcGIS items\n(Aug–Sep 2026). Full wildlife-area boundaries: Utah DWR.\nPositions & quotes: Weber Co. Commission & Planning Commission minutes\n(Mar 3, Jun 29, Aug 4 2026); West Haven minutes (Mar 4 2026); North\nLegacy Supplemental Study (2009); Weber Co. 2021 corridor map; Western\nWeber General Plan (2024); West Davis Corridor FEIS (2017).\nFull citations: docs/research/findings/2026-09-27.md', 'CONCEPTUAL RESEARCH EXHIBIT — not an official alignment, right-of-way,\nor parcel map. Do not use for property decisions.']
LH = 13 * 1.38 / 72 / FH
ny_ = ey - 0.008
for part in notes_parts:
    lines = part.split("\n")
    head, body = (lines[0], "\n".join(lines[1:])) if not part.startswith("CONCEPTUAL") else (None, part)
    if head:
        fig.text(px, ny_, head, fontsize=14, weight="bold", color=INK, va="top"); ny_ -= LH * 1.25
    fig.text(px, ny_, body, fontsize=13, color=INK2 if head else INK, va="top", linespacing=1.38,
             weight="normal" if head else "bold")
    ny_ -= LH * (body.count("\n") + 1) + LH * 0.9
fig.savefig(OUT + ".png", dpi=DPI, facecolor="white")
if "--pdf" in sys.argv:
    fig.savefig(OUT + ".pdf", facecolor="white")
print("saved", OUT, fig.get_size_inches() * DPI)

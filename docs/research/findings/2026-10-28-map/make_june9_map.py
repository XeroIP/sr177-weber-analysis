"""Routes named at the June 9, 2026 Weber County Planning Commission work session (research exhibit, 2026-10-28).

Usage: python3 make_june9_map.py DATA_DIR OUT [DPI] [--pdf]

DATA_DIR holds the JSON pulls made by ../2026-09-27-map/fetch.py
(jobs: counties munis streams lakes rail wfrc hdr dwr roads).

Only routes with a published location are drawn as lines. The minutes describe the
"red", "blue" and "purple" handout alignments only in words, so the strip above the
map shows what the minutes say about their east-west position and nothing more.
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Patch, Rectangle, FancyArrowPatch
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import shapely
from shapely.geometry import Polygon, LineString

DATA, OUT = sys.argv[1], sys.argv[2]
DPI = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 240

# ---------- projection: local equirectangular in km ----------
LAT0, LON0 = 41.24, -112.10
KX = 111.320 * np.cos(np.radians(LAT0))
KY = 110.95
def P(lon, lat):
    return (np.asarray(lon) - LON0) * KX, (np.asarray(lat) - LAT0) * KY

EXT = (-112.232, -111.968, 41.172, 41.382)   # lon min, lon max, lat min, lat max
x0, y0 = P(EXT[0], EXT[2]); x1, y1 = P(EXT[1], EXT[3])

# ---------- palette ----------
# Route hues follow the handout names in the minutes (green, red, blue, purple).
# Validated with the dataviz validator (--pairs all, light): all checks pass; the
# red/green CVD pair sits in the 6-8 warn band, so every route also carries a text label.
GREEN, RED, BLUE, PURPLE = "#008300", "#e34948", "#2a78d6", "#7d3fb0"
SURF = "#f4f3ef"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8984"
PLAN = "#1f1f1d"                                  # 8300 W general-plan option (no handout color)
WATER, WATER_LINE = "#d3e3f0", "#6f9fc8"
WMA_FILL, WMA_EDGE, WMA_TEXT = "#dfead7", "#8fae80", "#4d6b43"
halo = [pe.withStroke(linewidth=4, foreground="white")]
halo_s = [pe.withStroke(linewidth=3, foreground=SURF)]

def load(n):
    return json.load(open(os.path.join(DATA, n + ".json")))["features"]

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
wfrc = {f["attributes"]["OBJECTID"]: f for f in json.load(open(os.path.join(DATA, "wfrc_wwc.json")))["features"]}

def street_pos(name, idx):
    vals = []
    for f in roads:
        if f["attributes"]["FULLNAME"] == name:
            for pts in paths_of(f):
                m = shapely.contains_xy(weber, pts[:, 0], pts[:, 1])
                vals += list(pts[m][:, idx])
    return float(np.median(vals))

# Weber County grid: address -> coordinate (interpolated from UGRC centerlines)
NS = {w: street_pos(f"{w} W", 0) for w in [1900, 3500, 4700, 5100, 5900, 6700, 7500, 8300]}
EW = {-4600: street_pos("4600 S", 1), -4000: street_pos("4000 S", 1), -3300: street_pos("3300 S", 1),
      -2550: street_pos("2550 S", 1), -1800: street_pos("1800 S", 1), -1200: street_pos("12TH ST", 1),
      -900: street_pos("900 S", 1), 900: street_pos("900 N", 1), 1800: street_pos("1800 N", 1),
      2700: street_pos("2700 N", 1), 4000: street_pos("4000 N", 1)}
def lon_of(w):
    ks = sorted(NS); return float(np.interp(w, ks, [NS[k] for k in ks]))
def lat_of(a):   # a<0 south
    ks = sorted(EW); return float(np.interp(a, ks, [EW[k] for k in ks]))
def xw(w):
    return float(P(lon_of(w), LAT0)[0])

def chaikin(pts, it=3):
    pts = np.asarray(pts, float)
    for _ in range(it):
        q = 0.75 * pts[:-1] + 0.25 * pts[1:]; r = 0.25 * pts[:-1] + 0.75 * pts[1:]
        new = np.empty((2 * len(q), 2)); new[0::2] = q; new[1::2] = r
        pts = np.vstack([pts[0], new, pts[-1]])
    return pts

def orient_north(a):
    return a if a[0, 1] < a[-1, 1] else a[::-1]
def wline(oid):
    return orient_north(np.vstack([np.array(pa) for pa in wfrc[oid]["geometry"]["paths"]]))
seg_p2 = wline(54)    # Davis Co line -> 4000 S (current UDOT study segment, on 5100 W)
seg_p3 = wline(53)    # 4000 S -> 12th St/900 S
seg_unf = wline(52)   # 900 S -> I-15 north
green = np.vstack([seg_p3, seg_unf])
def nearest_on(seg, lat):
    i = int(np.argmin(np.abs(seg[:, 1] - lat))); return seg[i]

# ---------- figure ----------
FW, FH = 30.0, 22.5
fig = plt.figure(figsize=(FW, FH), facecolor="white")
MAP_L, MAP_B = 0.018, 0.03
map_h = 17.0 / FH
map_w = map_h * FH / FW * (x1 - x0) / (y1 - y0)
ax = fig.add_axes([MAP_L, MAP_B, map_w, map_h])
ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal")
ax.set_facecolor(SURF)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color(INK2); s.set_linewidth(1.2)

# water bodies
for f in load("lakes"):
    t = f["attributes"]["FType_Text"]
    col = WATER if t in ("Lake/Pond", "Reservoir") else "#e6eee4"
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor=col, edgecolor="none", zorder=1))

# state wildlife areas & conservation easements (Utah DWR)
for f in load("dwr_wma"):
    a = f["attributes"]
    if a["type_"] in ("Wildlife Management Area", "Waterfowl Management Area", "Conservation Easement") and (a["acres"] or 0) > 100:
        ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor=WMA_FILL, edgecolor=WMA_EDGE,
                               linewidth=0.9, zorder=1.4, alpha=0.95))

# municipalities
for f in load("munis"):
    ax.add_patch(PathPatch(rings_path(f["geometry"]["rings"]), facecolor="#ebe8e0", edgecolor="#b5b1a6",
                           linewidth=0.9, linestyle=(0, (4, 3)), zorder=2, alpha=0.9))

# roads
styles = {"1": ("#4f4e4a", 3.4, 6), "3": ("#6c6a64", 2.0, 5.5), "4": ("#6c6a64", 1.8, 5.5), "5": ("#6c6a64", 1.8, 5.5),
          "6": ("#7b7973", 1.4, 5.4), "7": ("#8e8c86", 0.7, 5.2), "8": ("#9f9d96", 0.95, 5), "10": ("#a7a59e", 0.8, 4.9)}
groups = {}
for f in roads:
    col, lw, z = styles.get(f["attributes"]["CARTOCODE"], ("#d0cec7", 0.35, 4))
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

# Weber River
for f in load("streams"):
    if f["attributes"]["GNIS_Name"] in ("Weber River", "Ogden River"):
        for pts in paths_of(f):
            xs, ys = P(pts[:, 0], pts[:, 1])
            ax.plot(xs, ys, color=WATER_LINE, lw=2.6, zorder=5.7, solid_capstyle="round")

# county lines
for name, f in counties.items():
    for r in f["geometry"]["rings"]:
        r = np.array(r); xs, ys = P(r[:, 0], r[:, 1])
        ax.plot(xs, ys, color="#6f6d67", lw=1.8, ls=(0, (10, 3, 2, 3, 2, 3)), zorder=6)

def plot_ll(a, **kw):
    xs, ys = P(a[:, 0], a[:, 1]); return ax.plot(xs, ys, **kw)

# HDR "SR177 Phase 4" study area (working GIS, neutral so it is not read as a route color)
hdr = load("hdr_study")[0]
ax.add_patch(PathPatch(rings_path(hdr["geometry"]["rings"]), facecolor=INK3, alpha=0.06, edgecolor="none", zorder=6.4))
ax.add_patch(PathPatch(rings_path(hdr["geometry"]["rings"]), facecolor="none", edgecolor=INK3, linewidth=2.6,
                       linestyle=(0, (7, 3)), zorder=6.5))

# east-west range guides for the minutes' "4700 to 8000 West"
for w in (4700, 8000):
    gx = xw(w)
    ax.plot([gx, gx], [P(0, lat_of(-4000))[1], y1], color=INK2, lw=1.5, ls=(0, (1, 3)), zorder=6.8, dash_capstyle="round")

# current UDOT study segment (ends ~4000 S): neutral casing + dark core
plot_ll(seg_p2, color="#cfcdc6", lw=24, zorder=7, solid_capstyle="butt")
plot_ll(seg_p2, color="#3d3c39", lw=4.5, zorder=7.2, solid_capstyle="butt")

# Map 1: general-plan corridor option along 8300 W (approx. redraw of county map, as in the 2026-09-27 exhibit)
loop = np.array([nearest_on(green, lat_of(-2300)), [lon_of(7500), lat_of(-2100)], [lon_of(8300), lat_of(-1850)],
                 [lon_of(8300), lat_of(-900)], [lon_of(8300), lat_of(1200)], [lon_of(7900), lat_of(1700)],
                 [lon_of(7100), lat_of(1950)], nearest_on(green, lat_of(2050))])
loop = chaikin(loop, 3)
plot_ll(loop, color="white", lw=7.5, zorder=8.6)
plot_ll(loop, color=PLAN, lw=4.2, ls=(0, (5, 2.2)), zorder=8.7)

# Map 2: GREEN, the 2009 preferred alignment (2009 preserved corridor geometry as carried in WFRC's RTP)
plot_ll(green, color="white", lw=10, zorder=8.9, solid_capstyle="round")
plot_ll(green, color=GREEN, lw=6.5, zorder=9, solid_capstyle="round")

# where the green line crosses state wildlife land (Aug 2026 county revision context)
glin = LineString(green)
ogden_bay = [f for f in load("dwr_wma") if f["attributes"]["name"] == "Ogden Bay WMA"][0]
cross = glin.intersection(rings_to_poly(ogden_bay["geometry"]["rings"]))
cross_pt = cross.centroid if not cross.is_empty else glin.interpolate(0.3, normalized=True)

# ---------- labels ----------
def T(lon, lat, s, **kw):
    x, y = P(lon, lat); kw.setdefault("zorder", 12); return ax.text(x, y, s, **kw)

for w in [3500, 4700, 5100, 5900, 6700, 7500, 8300]:
    T(lon_of(w) + 0.0009, 41.3735, f"{w} W", fontsize=12, color=INK2,
      rotation=90, ha="left", va="center", path_effects=halo_s, zorder=11)
for a, lab in [(-4000, "4000 S"), (-3300, "3300 S"), (-2550, "2550 S"), (-1800, "1800 S"), (-1200, "12th St"),
               (-900, "900 S"), (900, "900 N"), (1800, "1800 N"), (2700, "2700 N"), (4000, "4000 N")]:
    T(EXT[1] - 0.003, lat_of(a) + 0.0009, lab, fontsize=12, color=INK2, ha="right", va="bottom", path_effects=halo_s, zorder=11)

T(-112.0245, 41.322, "I-15", fontsize=15, weight="bold", color=INK, path_effects=halo)
T(-112.0225, 41.205, "I-15", fontsize=15, weight="bold", color=INK, path_effects=halo)
T(lon_of(4700) - 0.0012, lat_of(-3000), "SR-134 (4700 W)", fontsize=12, color=INK2, rotation=90, ha="right", path_effects=halo_s)
T(-112.214, 41.2548, "Union Pacific RR", fontsize=11.5, color=INK2, style="italic", path_effects=halo_s)
T(-112.228, 41.366, "Great Salt Lake", fontsize=15, color="#4f7fa8", style="italic", path_effects=halo_s)
T(-112.021, 41.371, "Willard Bay", fontsize=13, color="#4f7fa8", style="italic", path_effects=halo_s)
T(-112.061, 41.2235, "Weber River", fontsize=13, color="#3f6f98", style="italic", path_effects=halo_s, rotation=-28)
T(-112.186, 41.333, "Harold S. Crane WMA", fontsize=13, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)
T(-112.218, 41.212, "Ogden Bay WMA", fontsize=13, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)
T(-112.071, 41.3585, "Willard Bay\nUpland Game Area", fontsize=11.5, color=WMA_TEXT, style="italic", weight="bold", path_effects=halo_s)

for name, lon, lat in [("WEST HAVEN", -112.075, 41.2), ("ROY", -112.035, 41.18),
                       ("PLAIN CITY", -112.084, 41.3105), ("FARR WEST", -111.997, 41.309),
                       ("MARRIOTT-\nSLATERVILLE", -112.003, 41.2775)]:
    T(lon, lat, name, fontsize=15, color="#8a877e", weight="bold", ha="center", va="center", path_effects=halo_s, zorder=3)
for name, lon, lat in [("West Warren", -112.18, 41.296), ("Reese", -112.172, 41.262), ("Taylor", -112.085, 41.225),
                       ("West Weber", -112.083, 41.2595)]:
    T(lon, lat, name, fontsize=12.5, color="#8a877e", style="italic", ha="center", path_effects=halo_s, zorder=3)
# county labels either side of the Weber / Box Elder line, measured at the west edge
cl_lat = weber.intersection(LineString([(-112.215, 41.0), (-112.215, 41.6)])).bounds[3]
T(-112.228, cl_lat + 0.0012, "BOX ELDER CO.", fontsize=13, color="#3d3c39", weight="bold", path_effects=halo_s, va="bottom")
T(-112.228, cl_lat - 0.0012, "WEBER CO.", fontsize=13, color="#3d3c39", weight="bold", path_effects=halo_s, va="top")

def callout(lon, lat, tlon, tlat, text, color, fs=12.5, ha="left"):
    ax.annotate(text, xy=P(lon, lat), xytext=P(tlon, tlat), fontsize=fs, color=INK, ha=ha, va="center", zorder=13,
                linespacing=1.28, bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=color, lw=2.0, alpha=0.97),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, shrinkA=2, shrinkB=5, mutation_scale=18))

gpt = nearest_on(green, lat_of(1300))
callout(*gpt, -112.128, 41.2925,
        "GREEN — County's preferred alignment,\nadopted 2009 (handout map 2). Drawn from the\n"
        "2009 preserved corridor as carried in WFRC's\n2023–2050 RTP.", GREEN)
lpt = nearest_on(loop, lat_of(200))
callout(*lpt, -112.226, 41.282,
        "General plan option along 8300 West\n(handout map 1; approx. redraw of\nthe county's future streets map)", PLAN)
callout(cross_pt.x, cross_pt.y, -112.226, 41.236,
        "Aug 2026: county moved its plan line to\n“route around the state property and follow\n"
        "higher, drier ground.” Revised line not\npublished; adoption not confirmed.", WMA_TEXT)
callout(-112.0915, 41.2465, -112.060, 41.252,
        "Jun 9: Planning Commission's unanimous\nconsensus for “the more westerly corridor\nalignment.”"
        " Jun 29: County Commission\nletter to keep the freeway west of the\nWeber River.", WATER_LINE)
callout(-112.0838, 41.338, -112.058, 41.345,
        "HDR working map “SR177 Phase 4”\nstudy area (unofficial consultant GIS,\nAug–Sep 2026). No route lines in it.", INK2)
callout(*nearest_on(seg_p2, 41.181), -112.060, 41.1805,
        "Current UDOT study ends ≈4000 S.\nDraft study due Nov 6, 2026.", "#3d3c39")

# north arrow + scale bar (miles)
nx, ny = P(-111.978, 41.366)
ax.annotate("", xy=(nx, ny + 1.2), xytext=(nx, ny - 0.4), arrowprops=dict(arrowstyle="-|>", lw=2.4, color=INK, mutation_scale=30), zorder=14)
ax.text(nx, ny + 1.35, "N", ha="center", va="bottom", fontsize=18, weight="bold", color=INK, path_effects=halo, zorder=14)
sx, sy = P(-112.228, 41.176)
mi = 1.609344
for i in range(4):
    ax.add_patch(Rectangle((sx + i * mi, sy), mi, 0.18, facecolor=INK if i % 2 == 0 else "white", edgecolor=INK, lw=1, zorder=14))
for i in range(5):
    ax.text(sx + i * mi, sy + 0.32, f"{i}", ha="center", va="bottom", fontsize=12, color=INK, path_effects=halo, zorder=14)
ax.text(sx + 4 * mi + 0.35, sy + 0.1, "miles", va="center", fontsize=12, color=INK, path_effects=halo, zorder=14)

# ---------- east-west strip: what the minutes say about each route's position ----------
STRIP_B = MAP_B + map_h + 0.012
STRIP_H = 0.148
sax = fig.add_axes([MAP_L, STRIP_B, map_w, STRIP_H])
sax.set_xlim(x0, x1); sax.set_ylim(0, 5.2); sax.axis("off")
sax.add_patch(Rectangle((x0, 0), x1 - x0, 5.2, facecolor="#faf9f6", edgecolor=INK3, lw=1.0, zorder=0))
for w in (4700, 8000):
    sax.plot([xw(w), xw(w)], [0.55, 4.25], color=INK2, lw=1.5, ls=(0, (1, 3)), zorder=1, dash_capstyle="round")
# street ticks along the bottom of the strip, aligned with the map
sax.plot([x0, x1], [0.55, 0.55], color=INK3, lw=1.0, zorder=1)
for w, ha in [(1900, "center"), (3500, "center"), (4700, "left"), (5100, "right"), (5900, "center"),
              (6700, "center"), (7500, "center"), (8000, "center")]:
    sax.plot([xw(w), xw(w)], [0.42, 0.68], color=INK2, lw=1.2, zorder=2)
    sax.text(xw(w) + (-0.08 if ha == "right" else 0.08 if ha == "left" else 0), 0.33, f"{w} W", fontsize=11.5,
             color=INK if w in (4700, 8000) else INK2, ha=ha, va="top", weight="bold" if w in (4700, 8000) else "normal", zorder=2)
sax.text(x1 - 0.25, 0.75, "east →", fontsize=11.5, color=INK2, ha="right", va="bottom", style="italic")
sax.text(x0 + 0.25, 0.75, "← west", fontsize=11.5, color=INK2, ha="left", va="bottom", style="italic")
sax.text(x0 + 0.25, 4.95, "EAST–WEST POSITION OF EACH ROUTE, AS THE MINUTES DESCRIBE IT (aligned with the map below)",
         fontsize=13, weight="bold", color=INK, ha="left", va="top")

def range_bar(y, wa, wb, color, label):
    xa, xb = sorted((xw(wa), xw(wb)))
    sax.add_patch(Rectangle((xa, y - 0.2), xb - xa, 0.4, facecolor=color, alpha=0.2, edgecolor=color, lw=2.0,
                            ls=(0, (4, 2)), zorder=3))
    sax.text(xb + 0.3, y, label, fontsize=12.5, weight="bold", color=INK, ha="left", va="center", zorder=4)
range_bar(3.8, 4700, 8000, BLUE, "BLUE — UDOT alternative (handout map 3)")
range_bar(3.05, 4700, 8000, PURPLE, "PURPLE — UDOT alternative (handout map 3)")
sax.text(xw(4700) + 0.3, 3.42, "Minutes: “further east, in the range of 4700 to 8000 West.” Not published; not drawn.",
         fontsize=11.5, color=INK2, ha="left", va="center", style="italic", zorder=4)
# green: drawn; span from 5100 W at 4000 S to the drawn line's westmost point
def w_of(lon):
    ks = sorted(NS); return float(np.interp(-lon, [-NS[k] for k in ks], ks))
west_lon = float(green[:, 0].min())
west_w = int(round(w_of(west_lon) / 100) * 100)
gx_a, gx_b = float(P(west_lon, LAT0)[0]), xw(5100)
sax.add_patch(Rectangle((gx_a, 2.05), gx_b - gx_a, 0.34, facecolor=GREEN, edgecolor="white", lw=1.5, zorder=3))
sax.text(gx_b + 0.3, 2.22, f"GREEN — 2009 preferred (map 2): 5100 W at 4000 S, ≈{west_w} W at its westmost.  DRAWN",
         fontsize=12.5, weight="bold", color=INK, ha="left", va="center", zorder=4)
# red: only a direction relative to green
red_arrow = FancyArrowPatch((gx_a, 1.3), (x0 + 0.6, 1.3), arrowstyle="-|>", mutation_scale=22, color=RED, lw=2.4,
                            ls=(0, (4, 2)), zorder=3)
sax.add_patch(red_arrow)
sax.text(gx_a + 0.3, 1.3, "RED — county alternate (map 2): “further west” than green. No location given, so not drawn.",
         fontsize=12.5, weight="bold", color=INK, ha="left", va="center", zorder=4)

# ---------- side panel ----------
px = MAP_L + map_w + 0.02
pw = 1 - px - 0.012
pax = fig.add_axes([px, 0.03, pw, 0.94]); pax.axis("off"); pax.set_xlim(0, 1); pax.set_ylim(0, 1)
R = fig.canvas.get_renderer()
PB = pax.get_window_extent(renderer=R)

def put(x, y, s, **kw):
    """Draw top-aligned text in panel coords; return (artist, height, width) in panel fractions."""
    t = pax.text(x, y, s, va="top", **kw)
    bb = t.get_window_extent(renderer=R)
    return t, bb.height / PB.height, bb.width / PB.width

def para(y, s, gap=0.0, **kw):
    return y - put(0, y, s, **kw)[1] - gap

y = 1.0
y = para(y, "SR-177 north of West Haven:\nthe routes named on June 9, 2026", 0.012, fontsize=30, weight="bold",
         color=INK, linespacing=1.15)
y = para(y, "Weber County Planning Commission work session, “West Weber Freeway Corridor”\n"
            "(draft minutes, in the Oct 13, 2026 packet). Staff handed out three maps; none\n"
            "has been published. Only routes with a public location are drawn. As of Oct 28, 2026.",
         0.02, fontsize=15, color=INK2, linespacing=1.3)

y = para(y, "What the handout maps showed, per the minutes", 0.01, fontsize=16.5, weight="bold", color=INK)
rows = [
    ("line", PLAN, (0, (5, 2.2)), "Map 1 · Current general plan",
     "“two corridor options, including an alignment along 8300 West.”",
     "DRAWN (approx.):", "the 8300 West option, from the county's future streets map."),
    ("line", GREEN, "-", "Map 2 · GREEN, the county's preferred alignment", "“originally adopted in 2009.”",
     "DRAWN:", "2009 preserved corridor (WFRC RTP geometry). Treating it as the\nhandout's green line rests on the minutes' wording (inference)."),
    ("box", RED, None, "Map 2 · RED, county alternate", "an alternate “red” alignment “further west.”",
     "NOT DRAWN:", "location not published."),
    ("box", BLUE, None, "Map 3 · BLUE, UDOT alternative", "“further east, in the range of 4700 to 8000 West.”",
     "NOT DRAWN:", "location not published."),
    ("box", PURPLE, None, "Map 3 · PURPLE, UDOT alternative", "“further east, in the range of 4700 to 8000 West.”",
     "NOT DRAWN:", "location not published."),
]
TX = 0.075
for kind, color, ls, head, quote, key, rest in rows:
    _, h, _ = put(TX, y, head, fontsize=14.5, weight="bold", color=INK)
    sw_y = y - h * 0.55
    if kind == "line":
        pax.add_line(Line2D([0.0, 0.058], [sw_y, sw_y], color=color, lw=6 if color == GREEN else 4.2, ls=ls,
                            solid_capstyle="round"))
    else:
        pax.add_patch(Rectangle((0.0, sw_y - 0.0065), 0.058, 0.013, facecolor=color, alpha=0.2, edgecolor=color,
                                lw=2.0, ls=(0, (4, 2))))
    y -= h + 0.003
    _, h, _ = put(TX, y, quote, fontsize=13.5, color=INK2, style="italic")
    y -= h + 0.003
    _, hk, wk = put(TX, y, key, fontsize=13.5, weight="bold", color=INK)
    _, hr, _ = put(TX + wk + 0.008, y, rest, fontsize=13.5, color=INK, linespacing=1.3)
    y -= max(hk, hr) + 0.013

y -= 0.004
y = para(y, "On June 9", 0.006, fontsize=16.5, weight="bold", color=INK)
for t in ["Staff: UDOT “has not yet communicated a definitive preferred alignment.”",
          "Planning Commission: “unanimous consensus in support of the more westerly\ncorridor alignment,” with a formal letter to UDOT as the goal."]:
    put(0, y, "•", fontsize=13.5, color=INK2)
    y -= put(0.022, y, t, fontsize=13.5, color=INK2, linespacing=1.3)[1] + 0.005

y -= 0.008
y = para(y, "Since then", 0.006, fontsize=16.5, weight="bold", color=INK)
events = [
    ("Jun 29", "County Commission approves a letter: keep the freeway west of the Weber River"),
    ("Aug 4", "County staff show an alternative around state land and wetlands (not published)"),
    ("Aug 11", "County plan line revised to go around state property (not published)"),
    ("Sep 22", "County Commission agenda: general plan resolution naming the SR-177\ncorridor (adoption not confirmed as of Oct 28)"),
    ("Nov 6", "UDOT Draft State Environmental Study, 1800 N (West Point) → ≈4000 S"),
]
for d, t in events:
    put(0, y, d, fontsize=13.5, weight="bold", color=INK2)
    y -= put(0.09, y, t, fontsize=13.5, color=INK2, linespacing=1.3)[1] + 0.005

y -= 0.012
handles = [
    (Line2D([0], [0], color=GREEN, lw=6), "GREEN: county's 2009 preferred alignment"),
    (Line2D([0], [0], color=PLAN, lw=4.2, ls=(0, (5, 2.2))), "General plan option along 8300 West (approx.)"),
    (Line2D([0], [0], color="#3d3c39", lw=4.5), "Current UDOT study segment (5100 W, to ≈4000 S)"),
    (Patch(facecolor=(0.54, 0.54, 0.52, 0.06), edgecolor=INK3, lw=2.2, ls="--"), "HDR working-map study area (unofficial)"),
    (Line2D([0], [0], color=INK2, lw=1.5, ls=(0, (1, 3))), "4700 W and 8000 W: range quoted for blue & purple"),
    (Patch(facecolor=WMA_FILL, edgecolor=WMA_EDGE), "State wildlife areas & conservation easements"),
    (Line2D([0], [0], color=WATER_LINE, lw=2.6), "Weber River"),
    (Line2D([0], [0], color="#4f4e4a", lw=3.4), "Interstate"),
    (Line2D([0], [0], color="#6c6a64", lw=1.8), "State highways"),
    (Line2D([0], [0], color="#a7a59e", lw=0.9), "Local roads"),
    (Line2D([0], [0], color="#6f6d67", lw=1.1, ls=(0, (5, 2.5))), "Railroads"),
    (Patch(facecolor="#ebe8e0", edgecolor="#b5b1a6", ls="--"), "City limits"),
    (Line2D([0], [0], color="#6f6d67", lw=1.8, ls=(0, (10, 3, 2, 3, 2, 3))), "County line"),
]
leg_kw = dict(loc="upper left", frameon=False, fontsize=13.5, handleheight=1.2, labelspacing=0.6, borderaxespad=0,
              alignment="left", bbox_transform=pax.transAxes)
leg1 = pax.legend([h for h, _ in handles[:7]], [t for _, t in handles[:7]], bbox_to_anchor=(0, y), handlelength=3.6,
                  title="Legend", title_fontproperties={"size": 16.5, "weight": "bold"}, **leg_kw)
pax.add_artist(leg1)
leg2 = pax.legend([h for h, _ in handles[7:]], [t for _, t in handles[7:]], bbox_to_anchor=(0.66, y), handlelength=3.0,
                  title=" ", title_fontproperties={"size": 16.5, "weight": "bold"}, **leg_kw)
y -= max(l.get_window_extent(renderer=R).height for l in (leg1, leg2)) / PB.height + 0.018

src = ("Route descriptions & quotes: Weber Co. Planning Commission draft minutes, Jun 9, 2026\n"
       "(Oct 13, 2026 packet); Aug 11, 2026 minutes; Weber Co. Commission minutes, Jun 29, 2026;\n"
       "Sep 22, 2026 Commission packet. Green line: WFRC 2023–2050 RTP Roadway Projects layer\n"
       "(matches the 2009 North Legacy study and 2021 county corridor map). 8300 W option: Western\n"
       "Weber General Plan future streets map, redrawn by hand. Study area: public HDR ArcGIS item.\n"
       "Base map: UGRC roads, boundaries, NHD water, railroads; Utah DWR wildlife areas (Oct 2026).\n"
       "Full citations: docs/research/findings/2026-10-28.md")
y = para(y, "Sources", 0.004, fontsize=15, weight="bold", color=INK)
y = para(y, src, 0.016, fontsize=13, color=INK2, linespacing=1.33)
para(y, "CONCEPTUAL RESEARCH EXHIBIT — not an official alignment, right-of-way, or parcel map.\n"
        "The red, blue and purple routes are not drawn because their locations are not public.\n"
        "Do not use for property decisions.", fontsize=13.5, weight="bold", color=INK, linespacing=1.33)

fig.savefig(OUT + ".png", dpi=DPI, facecolor="white")
if "--pdf" in sys.argv:
    fig.savefig(OUT + ".pdf", facecolor="white")
print("saved", OUT, fig.get_size_inches() * DPI)

"""Download the public GIS layers used by make_map.py (Esri JSON, WGS84) into the current folder.
Usage: python3 fetch.py roads munis counties streams lakes rail power wfrc hdr dwr
"""
import json, subprocess, urllib.parse, sys, os
BBOX="-112.26,41.09,-111.94,41.40"
UG="https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services"
def get(url, params):
    q=urllib.parse.urlencode(params)
    r=subprocess.run(["curl","-sS","--max-time","120",url+"?"+q],capture_output=True,text=True)
    return json.loads(r.stdout)
def layer_fields(base):
    d=get(base,{"f":"json"}); return d.get("name"), [f["name"] for f in d.get("fields",[])], d.get("maxRecordCount",1000), d.get("geometryType")
def fetch(name, base, where="1=1", outFields="*", offset_tol=None, bbox=BBOX):
    nm, fields, mrc, gt = layer_fields(base)
    feats=[]; off=0
    while True:
        p={"where":where,"geometry":bbox,"geometryType":"esriGeometryEnvelope","inSR":"4326","spatialRel":"esriSpatialRelIntersects",
           "outFields":outFields,"returnGeometry":"true","outSR":"4326","f":"json","resultOffset":off,"resultRecordCount":mrc,"orderByFields":"OBJECTID" if "OBJECTID" in fields else ""}
        if offset_tol: p["maxAllowableOffset"]=offset_tol
        d=get(base+"/query",p)
        if "error" in d: print(name,"ERROR",d["error"]); break
        fs=d.get("features",[]); feats+=fs
        if not d.get("exceededTransferLimit") and len(fs)<mrc: break
        if not fs: break
        off+=len(fs)
    json.dump({"name":nm,"geometryType":gt,"features":feats},open(name+".json","w"))
    print(name, nm, gt, len(feats), "fields:", fields[:25])
jobs=sys.argv[1:]
if "roads" in jobs: fetch("roads", UG+"/UtahRoads/FeatureServer/0", outFields="FULLNAME,CARTOCODE,DOT_RTNAME,STATUS,NAME,POSTDIR,PREDIR", offset_tol=0.00002)
if "munis" in jobs: fetch("munis", UG+"/UtahMunicipalBoundaries/FeatureServer/0", offset_tol=0.00005)
if "counties" in jobs: fetch("counties", UG+"/UtahCountyBoundaries/FeatureServer/0", offset_tol=0.0001)
if "streams" in jobs: fetch("streams", UG+"/UtahStreamsNHD/FeatureServer/0", where="GNIS_Name IS NOT NULL", outFields="GNIS_Name,FType_Text,IsMajor", offset_tol=0.00003)
if "lakes" in jobs: fetch("lakes", UG+"/UtahLakesNHD/FeatureServer/0", where="AreaSqKm > 0.02", outFields="GNIS_Name,FType_Text,AreaSqKm", offset_tol=0.0001)
if "rail" in jobs: fetch("rail", UG+"/UtahRailroads/FeatureServer/0", offset_tol=0.00003)
if "wfrc" in jobs:
    W="https://services1.arcgis.com/taguadKoI1XFwivx/arcgis/rest/services/2023_2050_RTP_Roadway_Projects_lines/FeatureServer/0"
    json.dump(get(W+"/query",{"where":"OBJECTID IN (52,53,54,101,102)","outFields":"OBJECTID,name,begin_place,end_place,phase,future_lanes",
              "returnGeometry":"true","outSR":"4326","f":"json"}),open("wfrc_wwc.json","w")); print("wfrc ok")
if "hdr" in jobs:
    H="https://services.arcgis.com/04HiymDgLlsbhaV4/arcgis/rest/services"
    for nm,url in [("hdr_study",H+"/SR177_Study_Area/FeatureServer/22"),("hdr_wma",H+"/Waterfowl_Management_Areas/FeatureServer/24"),
                   ("hdr_lwcf",H+"/LWCF_Projects/FeatureServer/30")]:
        json.dump(get(url+"/query",{"where":"1=1","outFields":"*","returnGeometry":"true","outSR":"4326","f":"json","maxAllowableOffset":"0.00005"}),open(nm+".json","w")); print(nm,"ok")
if "dwr" in jobs:
    fetch("dwr_wma","https://services.arcgis.com/ZzrwjTRez6FJiOq4/arcgis/rest/services/ULTRA_Properties_2_view/FeatureServer/0",offset_tol=0.00005)
if "power" in jobs: fetch("power", UG+"/TransmissionLines/FeatureServer/0", offset_tol=0.00003)

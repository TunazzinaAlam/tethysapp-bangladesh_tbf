from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from .helper import get_sfp_forecast
import datetime as dt
from .app import BangladeshTbf as app
import urlparse, json, datetime, os
from django.http import JsonResponse, HttpResponse

geojson ={
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature",
             "properties": {"Station": "Panchgarh", "Long": 88.547, "Lat": 26.3295, "River": "Karatoa-Atrai-GGH",
                            "comid": 58532}, "geometry": {"type": "Point", "coordinates": [88.547, 26.3295]}},
            {"type": "Feature",
             "properties": {"Station": "Dalia", "Long": 89.0764, "Lat": 26.1248, "River": "Teesta", "comid": 59031},
             "geometry": {"type": "Point", "coordinates": [89.0764, 26.1248]}},
            {"type": "Feature",
             "properties": {"Station": "Noonkhawa", "Long": 89.7691, "Lat": 25.9198, "River": "Brahmaputra-Jamuna",
                            "comid": 59163}, "geometry": {"type": "Point", "coordinates": [89.7691, 25.9198]}},
            {"type": "Feature",
             "properties": {"Station": "Kurigram", "Long": 89.6704, "Lat": 25.8199, "River": "Dharla", "comid": 59502},
             "geometry": {"type": "Point", "coordinates": [89.6704, 25.8199]}},
            {"type": "Feature",
             "properties": {"Station": "Dinajpur", "Long": 88.618762, "Lat": 25.689237, "River": "Punarbhaba",
                            "comid": 59595}, "geometry": {"type": "Point", "coordinates": [88.618762, 25.689237]}},
            {"type": "Feature",
             "properties": {"Station": "Badarganj", "Long": 89.07, "Lat": 25.6749, "River": "Jamuneswari",
                            "comid": 59936}, "geometry": {"type": "Point", "coordinates": [89.07, 25.6749]}},
            {"type": "Feature",
             "properties": {"Station": "Gaibandha", "Long": 89.5346, "Lat": 25.3525, "River": "Gaghot", "comid": 60395},
             "geometry": {"type": "Point", "coordinates": [89.5346, 25.3525]}},
            {"type": "Feature",
             "properties": {"Station": "Lorergorh", "Long": 91.294, "Lat": 25.1914, "River": "Jadukata",
                            "comid": 60504}, "geometry": {"type": "Point", "coordinates": [91.294, 25.1914]}},
            {"type": "Feature",
             "properties": {"Station": "Durgapur", "Long": 90.6707, "Lat": 25.1176, "River": "Someswari",
                            "comid": 60519}, "geometry": {"type": "Point", "coordinates": [90.6707, 25.1176]}},
            {"type": "Feature",
             "properties": {"Station": "Nakuagaon", "Long": 90.2235, "Lat": 25.1917, "River": "Bhugai", "comid": 60528},
             "geometry": {"type": "Point", "coordinates": [90.2235, 25.1917]}},
            {"type": "Feature",
             "properties": {"Station": "Sarighat", "Long": 92.1214, "Lat": 25.0871, "River": "Sari-Gowain",
                            "comid": 60552}, "geometry": {"type": "Point", "coordinates": [92.1214, 25.0871]}},
            {"type": "Feature",
             "properties": {"Station": "Amalshid", "Long": 92.4787, "Lat": 24.8685, "River": "Kushiyara",
                            "comid": 60759}, "geometry": {"type": "Point", "coordinates": [92.4787, 24.8685]}},
            {"type": "Feature",
             "properties": {"Station": "Rohanpur", "Long": 88.3213, "Lat": 24.8203, "River": "Mahananda",
                            "comid": 60794}, "geometry": {"type": "Point", "coordinates": [88.3213, 24.8203]}},
            {"type": "Feature",
             "properties": {"Station": "Pankha", "Long": 88.0689, "Lat": 24.6442, "River": "Ganges", "comid": 61067},
             "geometry": {"type": "Point", "coordinates": [88.0689, 24.6442]}},
            {"type": "Feature",
             "properties": {"Station": "Sherpur", "Long": 91.6848, "Lat": 24.6277, "River": "Khushiyera",
                            "comid": 61094}, "geometry": {"type": "Point", "coordinates": [91.6848, 24.6277]}},
            {"type": "Feature",
             "properties": {"Station": "JuriSilghat", "Long": 92.1203, "Lat": 24.5898, "River": "Juri", "comid": 61159},
             "geometry": {"type": "Point", "coordinates": [92.1203, 24.5898]}},
            {"type": "Feature",
             "properties": {"Station": "Manu RB", "Long": 91.9406, "Lat": 24.4274, "River": "Manu", "comid": 61660},
             "geometry": {"type": "Point", "coordinates": [91.9406, 24.4274]}},
            {"type": "Feature",
             "properties": {"Station": "Shaestaganj", "Long": 91.476, "Lat": 24.2776, "River": "Khowai",
                            "comid": 62136}, "geometry": {"type": "Point", "coordinates": [91.476, 24.2776]}},
            {"type": "Feature",
             "properties": {"Station": "Comilla", "Long": 91.2013, "Lat": 23.4704, "River": "Gumti", "comid": 62712},
             "geometry": {"type": "Point", "coordinates": [91.2013, 23.4704]}},
            {"type": "Feature",
             "properties": {"Station": "Faridpur", "Long": 89.8344, "Lat": 23.5971, "River": "Kumar", "comid": 62717},
             "geometry": {"type": "Point", "coordinates": [89.8344, 23.5971]}}
        ]
    }

#@login_required()
def home(request):
    map_layers = []
    pointID = 0
    riverNm = ''
    if request.method == 'POST' and 'comid' in request.POST:
        pointID = str(request.GET['comid'])
    else:
        pointID = str(61067)
        riverNm = 'Ganga'
    # geoserver_engine = app.get_spatial_dataset_service(name='mainGeoserver', as_engine=True)
    # response = geoserver_engine.get_layer(layerID, debug=True)
    #
    # kmlurl = response['result']['wms']['kml']
    # parsedkml = urlparse.urlparse(kmlurl)
    # bbox = urlparse.parse_qs(parsedkml.query)['bbox'][0]
    # bboxitems = bbox.split(",")
    # box_left = float(bboxitems[0])
    # box_right = float(bboxitems[2])
    # box_top = float(bboxitems[3]) 
    # box_bottom = float(bboxitems[1])
    # centerlat = (box_left + box_right) / 2
    # centerlong = (box_top + box_bottom) / 2
    #
    # print ("--------------------------------------------------")
    # print (box_left)
    # print (box_right)
    # print(box_top)
    # print(box_bottom)
    # print ("--------------------------------------------------")
    box_left = 88.068900
    box_right = 92.478700
    box_top = 26.329500
    box_bottom = 23.470400
    centerlat = 90.061
    centerlong = 24.858

    # path = r'c:\users\kshakya\tethys\src\tethys_apps\tethysapp\bangladesh_tbf\'
    geojson_object = geojson

    geojson_layer = MVLayer(source='GeoJSON',
                            options=geojson_object,
                            legend_title='LEGENDS',
                            legend_extent=[box_left, box_bottom, box_right, box_top],
                            legend_classes=[
                                MVLegendClass('point', 'River Points', fill='#00FF00', stroke='#000000')
                            ],
                            layer_options = {
                                'style': {
                                    'image': {
                                        'circle': {
                                            'radius': 5,
                                            'fill': {'color': '#00FF00'},
                                            'stroke': {'color': '#000000', 'width': 1},
                                        }
                                    }
                                }
                            }
                            )

    map_layers.append(geojson_layer)

    view_options = MVView(
        projection='EPSG:4326',
        center=[centerlat, centerlong],
        zoom=7,
        maxZoom=18,
        minZoom=5
    )
    map_options = MapView(
        height='400px',
        width='100%',
        layers=map_layers,
        legend=True,
        view=view_options
    )
    tbf_plot = plotBack(pointID, riverNm)
    # print (tbf_plot)
    # tbf_plot = ''

    context = {'map_options': map_options,'tbf_plot': tbf_plot}
    # context = {'map_options': map_options}
    return render(request, 'bangladesh_tbf/home.html', context)

# def set_default(obj):
#     if isinstance(obj, set):
#         return list(obj)
#     raise TypeError

def plotMap(request):
    riverNm = ""
    comid = request.POST.get("comid", "")
    riverNm = getA(comid)
    return_obj = {}
    return_obj = plotNew(comid, riverNm)
    return HttpResponse(return_obj, content_type='application/json')
    #return JsonResponse(return_obj, safe=False)

def plotNew(id, riverNm):
    dateraw = []
    datemean = []
    valuemean = []
    valuestdupper = []
    valuestdlower = []
    valuelower = []
    valueupper = []
    return_obj = {}

    comid = id
    forecasttype = 'mean' # ------------------------------------------------------------------------------
    watermlstring = get_sfp_forecast(comid, forecasttype)
    waterml = (watermlstring.text).split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuemean.append(parser[1].split('<')[0])
    for e in dateraw:
        mydate = dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S")
        datemean.append(mydate)

    forecasttype = 'std_dev_range_upper'
    dateraw = []
    watermlstring = get_sfp_forecast(comid, forecasttype)
    waterml = (watermlstring.text).split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdupper.append(parser[1].split('<')[0])

    forecasttype = 'std_dev_range_lower'
    dateraw = []
    watermlstring = get_sfp_forecast(comid, forecasttype)
    waterml = (watermlstring.text).split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdlower.append(parser[1].split('<')[0])

    forecasttype = 'max'
    dateraw = []
    watermlstring = get_sfp_forecast(comid, forecasttype)
    waterml = (watermlstring.text).split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valueupper.append(parser[1].split('<')[0])

    forecasttype = 'min'
    dateraw = []
    watermlstring = get_sfp_forecast(comid, forecasttype)
    waterml = (watermlstring.text).split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuelower.append(parser[1].split('<')[0])

    return_obj["valuestdlower"] = (valuestdlower)
    return_obj["valuestdupper"] = (valuestdupper)
    return_obj["valueupper"] = (valueupper)
    return_obj["valuelower"] = (valuelower)
    return_obj["valuemean"] = (valuemean)
    return_obj["success"] = "success"
    return_obj["display_name"] = riverNm
    return_obj["dateTimewa"] = (datemean)

    return JsonResponse(return_obj) #discharge_time_series

def ganges(request):
    print ("SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFE andDDDDDDDDDDDDDDDDDDDDDDD sound")
    dateraw = []
    datemean = []

def plotBack(id, riverNm):
    dateraw = []
    datemean = []
    valuemean = []
    datehighres = []
    valuehighres = []
    datestdupper = []
    valuestdupper = []
    datestdlower = []
    valuestdlower = []
    dateupper = []
    valueupper = []
    datelower = []
    valuelower = []
    # This is where you can change the input and rerun to get a different stream, forecast configuration, and time
    # You can identify different comid's from the NHDPlus or use the NWM Forecast Viewer App at https://apps.hydroshare.org/apps/
    # This is my stream at location x
    #mean
    comid = id  #Ganges
    forecasttype = 'mean'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    #print (watermlstring)
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuemean.append(parser[1].split('<')[0])
    for e in dateraw:
        datemean.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #high_res
    dateraw = []

    forecasttype = 'high_res'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    #print (watermlstring)
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuehighres.append(parser[1].split('<')[0])
    for e in dateraw:
        datehighres.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #std_dev_range_upper
    dateraw = []

    forecasttype = 'std_dev_range_upper'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdupper.append(parser[1].split('<')[0])
    for e in dateraw:
        datestdupper.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #std_dev_range_lower
    dateraw = []

    forecasttype = 'std_dev_range_lower'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuestdlower.append(parser[1].split('<')[0])
    for e in dateraw:
        datestdlower.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #outer_range_upper
    dateraw = []

    forecasttype = 'max'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valueupper.append(parser[1].split('<')[0])
    for e in dateraw:
        dateupper.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))
    #outer_range_lower
    dateraw = []

    forecasttype = 'min'
    watermlstring = str(get_sfp_forecast(comid, forecasttype))
    waterml = watermlstring.split('dateTimeUTC="')
    waterml.pop(0)
    for e in waterml:
        parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
        dateraw.append(parser[0])
        valuelower.append(parser[1].split('<')[0])
    for e in dateraw:
        datelower.append(dt.datetime.strptime(e, "%Y-%m-%dT%H:%M:%S"))

        # Configure the time series Plot View

    discharge_time_series = []
    discharge_time_series1 = []
    formatter_string = "%m/%d/%Y"
    counter  = 0
    for item in datemean:
       # mytime = (dt.datetime.strptime(item, "%Y-%m-%dT%H:%M:%S"))
        discharge_time_series.append([item, float(valuemean[counter])])
        discharge_time_series1.append([item, float(valuestdupper[counter])])
        counter = counter + 1


    tbf_plot = TimeSeries(
            engine='highcharts',
            title=riverNm,
            y_axis_title='Discharge',
            y_axis_units='cms',
            spline=True,
            series=[
                {
                    'name': 'High',
                    'color': '#FF0000',
                    'data': discharge_time_series1,
                },
                {
                    'name': 'Mean',
                    'color': '#0066ff',
                    'data': discharge_time_series,
                },
            ],
            width='100%',
            height='300px'
        )
    return tbf_plot

    # context = {
    #
    #     'tbf_plot': tbf_plot
    # }
    # return render(request, 'bangladesh_tbf/Ganges.html', context)

def getA(comid):
    geojson_object = geojson
    for row in geojson_object["features"]:
        text= ""
        text1= ""
        for key, value in row["properties"].items():
            if (key == "Station"):
                text1 = str(value) + " station at "
            if  (key == "River"):
                text = str(value) + " river"
            if (key == "comid") and (value == int(comid)):
                return (text1 + text)
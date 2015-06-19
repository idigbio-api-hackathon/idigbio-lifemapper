from django.shortcuts import render
from django.http import HttpResponse
import csv
import idigbio
import json

def individualcount(request):
    sUrl = idigbio.IDIGBIO_API_BASE + "v2/search/records/?limit=1&no_attribution=1&fields=[%22uuid%22]"
    jdata = idigbio.wgetLoadJsonTime(sUrl)
    recordsTotal = "{:,}".format(jdata["itemCount"])

    icUrl = idigbio.IDIGBIO_API_BASE + "v2/summary/top/records/?top_fields=[%22individualcount%22]&count=10000"
    jdata = idigbio.wgetLoadJsonTime(icUrl)
    individualCountTotal = "{:,}".format(idigbio.multiplyKeyByItemCount(jdata, "individualcount"))

    icUrl = idigbio.IDIGBIO_API_BASE + "v2/summary/top/records/?top_fields=[%22individualcount%22,%22kingdom%22]&count=10000"
    jdata = idigbio.wgetLoadJsonTime(icUrl)
    dataList = idigbio.topJson2Table(jdata, "individualcount", "kingdom", True, 10)
    data = json.dumps(dataList)

    icUrl = idigbio.IDIGBIO_API_BASE + "v2/summary/top/records/?top_fields=[%22individualcount%22,%22kingdom%22]&count=10000&rq={%22individualcount%22:{%22type%22:%22range%22,%22lte%22:0}}"
    jdata = idigbio.wgetLoadJsonTime(icUrl)
    dataList = idigbio.topJson2Table(jdata, "individualcount", "kingdom", True, 0)
    datan = json.dumps(dataList)
    
    context = {'data': data,'datan': datan, 'recordsTotal': recordsTotal, 'individualCountTotal': individualCountTotal}
    return render(request, 'explore/index.html', context)

def download(request):
    # Create the HttpResponse object with the appropriate CSV header.
    case = request.GET.get('case')
    
    response = HttpResponse(content_type='text/csv')
    response['Set-Cookie'] = 'fileDownload=true; path=/'
    response['Content-Disposition'] = 'attachment; filename="' + case + '.csv"'
    if case == "individualCountNegative":
        # In this case we are looking for an additional parameter with the value
        lte = request.GET.get('lte')
        gt = request.GET.get('gt')
        king = request.GET.get('kingdom')
        rq = ""
        if lte:
            rq = ",%22lte%22:" + lte
        if gt:
            rq += ",%22gt%22:" + gt
        if rq != "":
            if king:
                rq = "rq={%22individualcount%22:{%22type%22:%22range%22" + rq + "},%22kingdom%22:" + king + "}&"
            else:
                rq = "rq={%22individualcount%22:{%22type%22:%22range%22" + rq + "}}&"
        fields = ["uuid", "data.dwc:occurrenceID", "data.dwc:institutionCode", "data.dwc:collectionCode", "data.dwc:catalogNumber", "data.dwc:family", "data.dwc:scientificname", "data.dwc:eventDate", "data.dwc:country", "data.dwc:stateProvince", "data.dwc:individualCount"]
        print "case", case, rq
        writer = csv.writer(response)
        writer.writerow(fields)
        offset = 0
        while True:
            icnUrl = idigbio.IDIGBIO_API_BASE + "v2/search/records/?" + rq+ "no_attribution=1&limit=" + str(idigbio.IDIGBIO_SEARCH_LIMIT) + "&offset=" + str(offset)
            jdata = idigbio.wgetLoadJsonTime(icnUrl)
            if jdata == None:
                break
            offset += len(jdata["items"])
            idigbio.json2Table(jdata, writer, fields)
            if offset >= jdata["itemCount"]:
                break
    return response

#total = 0
#records = 0
#count = 0
#queryRecords = int(j1["itemCount"])

#for k in j1["individualcount"]:
#    print k, j1["individualcount"][k]
#    if k == 0:
#        print "Suspicious count zero:", j1["individualcount"][k]["itemCount"]
#        total += int(j1["individualcount"][k]["itemCount"])
#    else:
#        total += int(k) * int(j1["individualcount"][k]["itemCount"])
#    records += int(j1["individualcount"][k]["itemCount"])
#    count += 1

#print "Histogram size:", count
#print "Total number of specimens:", total
#print "Total number of records:", records
#print "Total number of queried records:", queryRecords
#print "Specimens per record:", total / float(records)
#print "Total number of specimens including unknown cases:", queryRecords - records + total
#print "Specimens per record:", (queryRecords - records + total) / float(queryRecords)

#    data = [1, 2, 3]


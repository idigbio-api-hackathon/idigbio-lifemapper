import json
import time
import urllib
import urllib2

IDIGBIO_API_BASE = "http://beta-search.idigbio.org/"
IDIGBIO_SEARCH_LIMIT = 5000

# Wgets the content of the URL, and loads the content as JSON
def wgetLoadJsonTime(url):
    # Try to get data at least n times (in case the server is loaded and returning 504 - timeout)
    tries = 5
    data = []
    for i in range(0,tries):
        try:
            data = urllib2.urlopen(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
        except urllib2.HTTPError, e:
            if e.code == 400:
                print "HTTP Error:", e.code, url
                break
            print "HTTP Error:", e.code, url, "Retrying in", (i + 1), "seconds"
            time.sleep(i + 1)
            continue
        except urllib2.URLError, e:
            print "URL Error:", e.reason, url
            continue
        break
    j = None
    if data:
        j = json.load(data)
    return j

def topJson2Table(jdata, xField, yField=None, isXInt=False, collapseXTo=0):
    tdata = []
    yFieldCats = {}
    if yField:
        for xkey in jdata[xField]:
            for ykey in jdata[xField][xkey][yField]:
                yFieldCats[ykey] = True
    yFieldCatsSorted = yFieldCats.keys()
    yFieldCatsSorted.sort()
    tdata.append([xField] + yFieldCatsSorted)
    print tdata

    if isXInt:
        xFieldCatsSorted = [ int(d) for d in jdata[xField].keys()]
    else:
        xFieldCatsSorted = jdata[xField].keys()
    xFieldCatsSorted.sort()

    if collapseXTo:
        itemsPerCat = len(xFieldCatsSorted) / collapseXTo
    else:
        itemsPerCat = 1
    xCount = 1
    counts = [0] * len(yFieldCatsSorted)
    isFirst = True
    for xkey in xFieldCatsSorted:
        if isFirst:
            catDesc = str(xkey)
            isFirst = False
        for yid, ykey in enumerate(yFieldCatsSorted):
            if isXInt:
                if ykey in jdata[xField][str(xkey)][yField]:
                    counts[yid] += jdata[xField][str(xkey)][yField][ykey]["itemCount"]
            else:
                if ykey in jdata[xField][xkey][yField]:
                    counts[yid] += jdata[xField][xkey][yField][ykey]["itemCount"]
        if xCount % itemsPerCat == 0:
            if itemsPerCat > 1:
                tdata.append([catDesc + "~" + str(xkey)] + counts)
            else:
                tdata.append([str(xkey)] + counts)
            counts = [0] * len(yFieldCatsSorted)
            isFirst = True
        xCount += 1
    return tdata

def tryEncode(s):
    try:
        if isinstance(s, unicode):
            return s.encode('utf-8')
        else:
            return s
    except Exception, e:
        print('Exception in encoding {0} {1}'.format(type(e), str(e)))
        return ''

def json2Table(jdata, writer, fields):

    for item in jdata["items"]:
        row = []
        for field in fields:
            if field.startswith('data.'):
                subfields = field.split(".")
                if subfields[1] in item["data"]:
                    row.append(tryEncode(item["data"][subfields[1]]))
                else:
                    row.append("")
            else:
                if field in item["indexTerms"]:
                    row.append(tryEncode(item["indexTerms"][field]))
                else:
                    row.append("")
        writer.writerow(row)

def multiplyKeyByItemCount(jdata, keyField):
    total = 0
    yFieldCats = {}
    if keyField in jdata:
        for key in jdata[keyField]:
            total += int(key) * jdata[keyField][key]["itemCount"]
    return total

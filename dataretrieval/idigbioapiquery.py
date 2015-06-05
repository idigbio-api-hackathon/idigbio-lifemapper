#!/usr/bin/env python

"""
@summary: Module containing functions for API Queries
@status: beta

@license: gpl2
@copyright: Copyright (C) 2014, University of Kansas Center for Research

          Lifemapper Project, lifemapper [at] ku [dot] edu, 
          Biodiversity Institute,
          1345 Jayhawk Boulevard, Lawrence, Kansas, 66045, USA
   
          This program is free software; you can redistribute it and/or modify 
          it under the terms of the GNU General Public License as published by 
          the Free Software Foundation; either version 2 of the License, or (at 
          your option) any later version.
  
          This program is distributed in the hope that it will be useful, but 
          WITHOUT ANY WARRANTY; without even the implied warranty of 
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
          General Public License for more details.
  
          You should have received a copy of the GNU General Public License 
          along with this program; if not, write to the Free Software 
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
          02110-1301, USA.

@copyright: Copyright (C) 2015, University of Florida, iDigBio project
"""
import csv
import json
import os
import re
import shelve
import time
import urllib, urllib2, urlparse
from types import BooleanType, FloatType, IntType, ListType, TupleType, StringType 

from idigbioconstants import URL_ESCAPES, BINOMIAL_REGEX, INVALIDSP_REGEX, \
        IDIGBIO_SEARCH_URL_PREFIX, IDIGBIO_PUBLISHERS_SEARCH_URL_PREFIX, \
        IDIGBIO_RECORDSETS_SEARCH_URL_PREFIX, IDIGBIO_AGG_SPECIES_GEO_MIN_40, \
        IDIGBIO_SPECIMENS_BY_BINOMIAL, IDIGBIO_RECORSETS, IDIGBIO_FIRST_10K, \
        IDIGBIO_QFILTERS, IDIGBIO_FILTERS

# .............................................................................
class APIQuery(object):
   """
   Class to query APIs and return results
   """
   def __init__(self, baseurl, 
                qFilters={}, otherFilters={}, filterString=None, 
                headers={}):
      """
      @summary Constructor for the APIQuery class
      """
      self.headers = headers
      # No added filters are on url (unless initialized with filters in url)
      self.baseurl = baseurl
      self._qFilters = qFilters
      self._otherFilters = otherFilters
      self.filterString = self._assembleFilterString(filterString=filterString)
      self.output = None
      self.debug = False
      
# ...............................................
   @classmethod
   def initFromUrl(cls, url, headers={}):
      base, filters = url.split('?')
      qry = APIQuery(base, filterString=filters)
      return qry
      
   # .........................................
   @property
   def url(self):
      # All filters added to url
      return '%s?%s' % (self.baseurl, self.filterString)

# ...............................................
   def addFilters(self, qFilters={}, otherFilters={}):
      """
      @summary: Add new or replace existing filters.  This does not remove 
                existing filters, unless existing keys are sent with new values.
      """
      self.output = None
      for k, v in qFilters.iteritems():
         self._qFilters[k] = v
      for k, v in otherFilters.iteritems():
         self._otherFilters[k] = v
      self.filterString = self._assembleFilterString()
         
# ...............................................
   def clearAll(self, qFilters=True, otherFilters=True):
      """
      @summary: Clear existing qFilters, otherFilters, and output
      """
      self.output = None
      if qFilters:
         self._qFilters = {}
      if otherFilters:
         self._otherFilters = {}
      self.filterString = self._assembleFilterString()

# ...............................................
   def clearOtherFilters(self):
      """
      @summary: Clear existing otherFilters and output
      """
      self.clearAll(otherFilters=True, qFilters=False)

# ...............................................
   def clearQFilters(self):
      """
      @summary: Clear existing qFilters and output
      """
      self.clearAll(otherFilters=False, qFilters=True)

# ...............................................
   def _assembleFilterString(self, filterString=None):
      if filterString is not None:
         for replaceStr, withStr in URL_ESCAPES:
            filterString = filterString.replace(replaceStr, withStr)
      else:
         allFilters = self._otherFilters.copy()
         if self._qFilters:
            qVal = self._assembleQVal(self._qFilters)
            allFilters['q'] = qVal
         filterString = self._assembleKeyValFilters(allFilters)
      return filterString

# ...............................................
   def _assembleKeyValFilters(self, ofDict):
      for k, v in ofDict.iteritems():
         if isinstance(v, BooleanType):
            v = str(v).lower()
         ofDict[k] = unicode(v).encode('utf-8')               
      filterString = urllib.urlencode(ofDict)
      return filterString
      
# ...............................................
   def _interpretQClause(self, key, val):
      cls = None
      if (isinstance(val, StringType) or 
          isinstance(val, IntType) or 
          isinstance(val, FloatType)):
         cls = '%s:%s' % (key, str(val))
      # Tuple for negated or range value
      elif isinstance(val, TupleType):            
         # negated filter
         if isinstance(val[0], BooleanType) and val[0] is False:
            cls = 'NOT ' + key + ':' + str(val[1])
         # range filter (better be numbers)
         elif ((isinstance(val[0], IntType) or isinstance(val[0], FloatType))
               and (isinstance(val[1], IntType) or isinstance(val[1], FloatType))):
            cls = '%s:[%s TO %s]' % (key, str(val[0]), str(val[1]))
         else:
            print 'Unexpected value type %s' % str(val)
      else:
         print 'Unexpected value type %s' % str(val)
      return cls
   
# ...............................................
   def _assembleQItem(self, key, val):
      itmClauses = []
      # List for multiple values of same key
      if isinstance(val, ListType):
         for v in val:
            itmClauses.append(self._interpretQClause(key, v))
      else:
         itmClauses.append(self._interpretQClause(key, val))
      return itmClauses

# ...............................................
   def _assembleQVal(self, qDict):
      clauses = []
      qval = ''
      # interpret dictionary
      for key, val in qDict.iteritems():
         clauses.extend(self._assembleQItem(key, val))
      # convert to string
      firstClause = None
      for cls in clauses:
         if not firstClause and not cls.startswith('NOT'):
            firstClause = cls
         elif cls.startswith('NOT'):
            qval = ' '.join((qval, cls))
         else:
            qval = ' AND '.join((qval, cls))
      qval = firstClause + qval
      return qval

# ...............................................
   def query(self, outputType='json'):
#       # Also Works
#       response = urllib2.urlopen(fullUrl.decode('utf-8'))
      data = None
      if self._qFilters:
         # All q and other filters are on url
         req = urllib2.Request(self.url, None, self.headers)
      else:
         if self._otherFilters:
            data = urllib.urlencode(self._otherFilters)
         # Any filters are in data
         req = urllib2.Request(self.url, data, self.headers)
      response = urllib2.urlopen(req)
      output = response.read()
      if outputType == 'json':
         import json
         try:
            self.output = json.loads(output)
         except Exception, e:
            print str(e)
            raise
      elif outputType == 'xml':
         try:
            root = ET.fromstring(output)
            self.output = root    
         except Exception, e:
            print str(e)
            raise
      else:
         print 'Unrecognized output type %s' % str(outputType)
         self.output = None  

# .............................................................................
class IdigbioAPI(APIQuery):
# .............................................................................
   """
   Class to query iDigBio APIs and return results
   """
# ...............................................
   def __init__(self, url, qFilters={}, otherFilters={}, filterString=None,
                headers={'Content-Type': 'application/json'}):
      """
      @summary: Constructor for IdigbioAPI class      
      """
      # Add Q filters for this instance
      for key, val in IDIGBIO_QFILTERS.iteritems():
         qFilters[key] = val
      # Add other filters for this instance
      for key, val in IDIGBIO_FILTERS.iteritems():
         otherFilters[key] = val
         
      APIQuery.__init__(self, url, qFilters=qFilters, 
                        otherFilters=otherFilters, filterString=filterString, 
                        headers=headers)
      
# ...............................................
   @classmethod
   def initFromUrl(cls, url, headers={'Content-Type': 'application/json'}):
      base, filters = url.split('?')
      if base == IDIGBIO_SEARCH_URL_PREFIX:
         qry = IdigbioAPI(filterString=filters)
      else:
         raise Exception('iDigBio occurrence API must start with %s' 
                         % IDIGBIO_SEARCH_URL_PREFIX)
      return qry
      
# ...............................................
   def _burrow(self, keylst):
      dict = self.output
      for key in keylst:
         dict = dict[key]
      return dict
         
# ...............................................
   def getBinomial(self):
      """
      @summary: Returns a list of dictionaries where each dictionary is an 
                occurrence record
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      dataList = self._burrow(["aggregations", "my_agg", "buckets"])
      binomialList = []
      filtered = []
      print 'Distinct scientific names count = %d' % (len(dataList))
      for entry in dataList:
         matches = re.match(BINOMIAL_REGEX, entry["key"])
         if matches:
            for invsp in INVALIDSP_REGEX:
               if re.match(invsp, matches.group(2)):
                  break
                  if self.debug:
                     filtered.append(entry["key"])
            else: # Valid binomial case
               binomialList.append(entry)
         else:
            if self.debug:
               filtered.append(entry["key"])
      print 'Distinct binomials count = %d' % (len(binomialList))
      if self.debug:
         print 'Filtered:', filtered
      return binomialList

# ...............................................
   def getSpecimensByBinomial(self):
      """
      @summary: Returns a list of dictionaries.  Each dictionary is an occurrence record
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      specimenList = []
      attributionDict = {}
      dataList = self._burrow(["hits", "hits"])
      for entry in dataList:
         provider = ''
         if "data" in entry["_source"]:
             if "dwc:institutionCode" in entry["_source"]["data"]["idigbio:data"]:
                 provider = entry["_source"]["data"]["idigbio:data"]["dwc:institutionCode"]
             if "dwc:collectionCode" in entry["_source"]["data"]["idigbio:data"]:
                 provider += ':' + entry["_source"]["data"]["idigbio:data"]["dwc:collectionCode"]
         entry["fields"]["provider"] = [provider]
         specimenList.append(entry["fields"])
      dataList = self._burrow(["aggregations", "filtered_agg", "my_agg", "buckets"])
      for entry in dataList:
         attributionDict[entry["key"]] = {"doc_count" : entry["doc_count"]}
      return specimenList, attributionDict

# ...............................................
   def getPublishers(self):
      """
      @summary: Returns a dictionary. Dictionary key is publisher UUID and value is publisher's name
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      publishersDict = {}
      dataList = self._burrow(["hits", "hits"])
      for entry in dataList:
         if entry["_source"]["data"]["idigbio:data"]["name"]:
            if entry["_source"]["data"]["idigbio:data"]["name"].startswith("http"):
               publishersDict[entry["_source"]["uuid"]] = urlparse.urlparse(entry["_source"]["data"]["idigbio:data"]["base_url"]).hostname
            else:
               publishersDict[entry["_source"]["uuid"]] = entry["_source"]["data"]["idigbio:data"]["name"]
         else:
            publishersDict[entry["_source"]["uuid"]] = urlparse.urlparse(entry["_source"]["data"]["idigbio:data"]["base_url"]).hostname
      return publishersDict

# ...............................................
   def getRecordsets(self, publishers):
      """
      @summary: Returns a dictionary with recordset UUID as key and a dictionary with recordset information as value
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      recordsetsDict = {}
      dataList = self._burrow(["hits", "hits"])
      for entry in dataList:
         recordsetsDict[entry["_source"]["uuid"]] = entry["_source"]["data"]["idigbio:data"]
         recordsetsDict[entry["_source"]["uuid"]]["publisher"] = entry["_source"]["publisher"]
         recordsetsDict[entry["_source"]["uuid"]]["publisherName"] = publishers[entry["_source"]["publisher"]]
      return recordsetsDict

# ...............................................
   def query(self):
      """
      @summary: Queries the API and sets 'output' attribute to a JSON object 
      """
      APIQuery.query(self, outputType='json')
      
      
# .............................................................................
# Main method to (a) retrieve all scientific names in iDigBio, (b) keep only
# binomials, (c) for each binomial create a list of other names to be included
# (usually subspecies and names with authors), and (d) retrieve occurrences
# for each species.
# .............................................................................

if __name__ == '__main__':
   folder = "iDigBio_" + time.strftime("%Y%m%d")
   if not os.path.exists(folder):
      os.makedirs(folder)

   publishersQuery = IdigbioAPI(IDIGBIO_PUBLISHERS_SEARCH_URL_PREFIX, filterString="source=" + IDIGBIO_FIRST_10K)
   publishers = publishersQuery.getPublishers()
   recordsetsQuery = IdigbioAPI(IDIGBIO_RECORDSETS_SEARCH_URL_PREFIX, filterString="source=" + IDIGBIO_FIRST_10K)
   recordsets = recordsetsQuery.getRecordsets(publishers)
   print len(recordsets)
   scinameQuery = IdigbioAPI(IDIGBIO_SEARCH_URL_PREFIX, filterString="source=" + IDIGBIO_AGG_SPECIES_GEO_MIN_40)
   binomials = scinameQuery.getBinomial()
   #print binomials
   f = open(folder + '/' + 'binomials.csv','wb')
   fw = csv.writer(f, dialect='excel')
   fw.writerow(["scientificname", "doc_count"])
   for id, binomial in enumerate(binomials):
      fw.writerow([binomial["key"].encode('utf-8'), binomial["doc_count"]])
   f.close()
   f2 = open(folder + '/' + 'binomialsAccepted.csv','wb')
   fw2 = csv.writer(f2, dialect='excel')
   fw2.writerow(["scientificname", "doc_count", "specimen_count"])

   for id, binomial in enumerate(binomials):
      if id > 100000:
         quit()
      else:
         binomialStripped = re.sub("[\"()?/.]", "", binomial["key"])
         binFolder = folder + "/" + binomialStripped
         specimenQuery = IdigbioAPI(IDIGBIO_SEARCH_URL_PREFIX, filterString="source=" + IDIGBIO_SPECIMENS_BY_BINOMIAL.replace("__BINOMIAL__", binomial["key"].encode('utf-8').replace('"', '\\"')))
         specimens, attribution = specimenQuery.getSpecimensByBinomial()
         if len(specimens) < 40:
            print "ERROR: Binomial:", binomial["key"], " with unexpected minimum number of occurrences:", len(specimens), "Expected:", binomial["doc_count"]
            continue
         if not os.path.exists(binFolder):
            os.makedirs(binFolder)
         f = open(binFolder + '/' + binomialStripped + '_sp.csv','wb')
         fw = csv.writer(f, dialect='excel')
         fw.writerow(["uuid", "geopoint.lat", "geopoint.lon", "scientificname", "provider"])
         for specimen in specimens:
            fw.writerow([specimen["uuid"][0], specimen["geopoint.lat"][0], specimen["geopoint.lon"][0], specimen["scientificname"][0].encode('utf-8'), specimen["provider"][0].encode('utf-8')])
         f.close()
         for uuid in attribution.iterkeys():
            attribution[uuid].update(recordsets[uuid])
         with open(binFolder + '/' + binomialStripped + '_attr.json', 'w') as f:
            json.dump(attribution, f, indent=4, separators=(',', ': '))
            f.close()
         print "Retrieved %d specimens as %s" % (len(specimens), binomial["key"])
         fw2.writerow([binomial["key"].encode('utf-8'), binomial["doc_count"], len(specimens)])
   f2.close()


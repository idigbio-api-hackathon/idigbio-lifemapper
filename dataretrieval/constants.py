from osgeo.ogr import OFTInteger, OFTReal, OFTString

# ......................................................
GBIF_TAXON_FIELDS = {0: ('taxonkey', OFTString), 
                     1: ('kingdom', OFTString),
                     2: ('phylum', OFTString),
                     3: ('class', OFTString), 
                     4: ('order', OFTString),
                     5: ('family', OFTString),
                     6: ('genus', OFTString),
                     7: ('sciname', OFTString),
                     8: ('genuskey', OFTInteger),
                     9: ('specieskey', OFTInteger),
                     10:('count', OFTInteger)
                     }

GBIF_EXPORT_FIELDS = {0: ('gbifid', OFTInteger), 
                      1: ('occurid', OFTInteger), 
                      2: ('taxonkey', OFTInteger),
                      3: ('datasetkey', OFTString),
                      4: ('puborgkey', OFTString),
                      5: ('basisofrec', OFTString),
                      6: ('kingdomkey', OFTInteger),
                      7: ('phylumkey', OFTInteger),
                      8: ('classkey', OFTInteger),
                      9: ('orderkey', OFTInteger),
                      10: ('familykey', OFTInteger), 
                      11: ('genuskey', OFTInteger),
                      12: ('specieskey', OFTInteger),
                      13: ('sciname', OFTString),
                      14: ('dec_lat', OFTReal),
                      15: ('dec_long', OFTReal),
                      16: ('day', OFTInteger),
                      17: ('month', OFTInteger),
                      18: ('year', OFTInteger),
                      19: ('rec_by', OFTString)
                    }

GBIF_TAXONKEY_FIELD = 'specieskey'
GBIF_TAXONNAME_FIELD = 'sciname'
GBIF_PROVIDER_FIELD = 'puborgkey'

# .............................................................................
# .                              Time constants                               .
# .............................................................................
# Time constants in Modified Julian Day (MJD) units 
ONE_MONTH = 1.0 * 30
ONE_DAY = 1.0
ONE_HOUR = 1.0/24.0
ONE_MIN = 1.0/1440.0
ONE_SEC = 1.0/86400.0

# ......................................................
# For querying GBIF REST service for data
# ......................................................
# seconds to wait before retrying unresponsive services
GBIF_WAIT_TIME = 3 * ONE_MIN
GBIF_LIMIT = 300
GBIF_REST_URL = 'http://api.gbif.org/v1'
GBIF_SPECIES_SERVICE = 'species'
GBIF_OCCURRENCE_SERVICE = 'occurrence'
GBIF_DATASET_SERVICE = 'dataset'

GBIF_REQUEST_SIMPLE_QUERY_KEY = 'q'
GBIF_REQUEST_NAME_QUERY_KEY = 'name'
GBIF_REQUEST_TAXON_KEY = 'TAXON_KEY'
GBIF_REQUEST_RANK_KEY = 'rank'
GBIF_REQUEST_DATASET_KEY = 'dataset_key'                

GBIF_DATASET_BACKBONE_VALUE = 'GBIF Backbone Taxonomy'

GBIF_SEARCH_COMMAND = 'search'
GBIF_COUNT_COMMAND = 'count'
GBIF_MATCH_COMMAND = 'match'
GBIF_DOWNLOAD_COMMAND = 'download'
GBIF_DOWNLOAD_REQUEST_COMMAND = 'request'

GBIF_QUERY_PARAMS = {GBIF_SPECIES_SERVICE: {'status': 'ACCEPTED',
                                            GBIF_REQUEST_RANK_KEY: None,
                                            GBIF_REQUEST_DATASET_KEY: None,
                                            GBIF_REQUEST_NAME_QUERY_KEY: None},
                     GBIF_OCCURRENCE_SERVICE: {"GEOREFERENCED": True,
                                               "SPATIAL_ISSUES": False,
#                                                "BASIS_OF_RECORD": ["PRESERVED_SPECIMEN"],
                                               GBIF_REQUEST_TAXON_KEY: None},
                     GBIF_DOWNLOAD_COMMAND: {"creator": "aimee",
                                             "notification_address": ["lifemapper@mailinator.com"]}
                     }
URL_ESCAPES = [ [" ", "%20"] ]


GBIF_RESPONSE_IDENTIFIER_KEY = 'key'
GBIF_RESPONSE_RESULT_KEY = 'results'
GBIF_RESPONSE_END_KEY = 'endOfRecords'
GBIF_RESPONSE_COUNT_KEY = 'count'
GBIF_RESPONSE_GENUS_ID_KEY = 'genusKey'
GBIF_RESPONSE_GENUS_KEY = 'genus'
GBIF_RESPONSE_SPECIES_ID_KEY = 'speciesKey'
GBIF_RESPONSE_SPECIES_KEY = 'species'
GBIF_RESPONSE_MATCH_KEY = 'matchType'
GBIF_RESPONSE_NOMATCH_VALUE = 'NONE'

# For writing files from GBIF DarwinCore download, 
# DWC translations in lmCompute/code/sdm/gbif/constants
# We are adding these 2 fields
LM_WKT_FIELD = 'geomwkt'
GBIF_LINK_FIELD = 'gbifurl'

# What is the id field? BISON has none
GBIF_ID_FIELD = 'gbifid'
LM_ID_FIELD = 'lmid'

# Everyone likes DarwinCore!
DWC_X_FIELD = 'dec_long'
DWC_Y_FIELD = 'dec_lat'

GBIF_OCCURRENCE_URL = 'http://www.gbif.org/occurrence/'

# .............................................................................
# .                               BISON/ITIS constants                              .
# .............................................................................
# ......................................................
# For parsing BISON Solr API response, updated Oct 2014
# ......................................................
"""
http://bisonapi.usgs.ornl.gov/solr/occurrences/select/?
q=hierarchy_homonym_string:*%5C-202422%5C-*%20
  AND%20decimalLatitude:%5b0%20TO%2090%5d%20
  NOT%20basisOfRecord:living%20
  NOT%20basisOfRecord:fossil
&rows=5000000
&wt=json
&json.nl=arrarr
&indent=true
"""
BISON_OCCURRENCE_URL = 'http://bisonapi.usgs.ornl.gov/solr/occurrences/select/'
# For debugging:
# BISON_MIN_POINT_COUNT = 20000
# BISON_MAX_COUNT = 40
# For TSN query filtering on Binomial
BISON_NAME_KEY = 'ITISscientificName'
# For Occurrence query by TSN in hierarchy
BISON_HIERARCHY_KEY = 'hierarchy_homonym_string'
BISON_KINGDOM_KEY = 'kingdom'
BISON_TSN_KEY = 'TSNs'
# key = returned field name; val = (lmname, ogr type)
BISON_RESPONSE_FIELDS = {'computedCountyFips': None,
                        'providerID': None,
                        'catalogNumber': ('catnum', OFTString),
                        'basisOfRecord': ('basisofrec', OFTString),
                        'countryCode': ('ctrycode', OFTString),
                        BISON_NAME_KEY: ('sciname', OFTString),
                        'latlon': ('latlon', OFTString),
                        'calculatedState': ('state', OFTString),
                        'decimalLongitude':('dec_long', OFTReal),
                        'ITIStsn': ('itistsn', OFTInteger),
                        BISON_HIERARCHY_KEY: ('tsn_hier', OFTString),
                        BISON_TSN_KEY: None,
                        'calculatedCounty': ('county', OFTString),
                        'pointPath': None,
                        'computedStateFips': None,
                        'providedCounty': None,
                        BISON_KINGDOM_KEY: ('kingdom', OFTString),
                        'decimalLatitude': ('dec_lat', OFTReal),
                        'collectionID': ('collid', OFTString),
                        'occurrenceID': ('occurid', OFTInteger),
                        'providedScientificName': None,
                        'ownerInstitutionCollectionCode': ('instcode', OFTString),
                        'provider': ('provider', OFTString),
                        'ambiguous': None,
                        'resourceID': None,
                        'stateProvince': ('stprov', OFTString),
                        'ITIScommonName': ('comname', OFTString),
                        'scientificName': None,
                        'institutionID': ('instid', OFTString),
                        # Very long integer
                       '_version_': None
                        }

BISON_MIN_POINT_COUNT = 20
BISON_MAX_COUNT = 5000000
BISON_BBOX = (24, -125, 50, -66)

BINOMIAL_REGEX = '/[A-Za-z]*[ ]{1,1}[A-Za-z]*/'
BISON_TSN_FILTERS = {'facet': True,
                     'facet.limit': -1,
                     'facet.mincount': BISON_MIN_POINT_COUNT,
                     'facet.field': BISON_TSN_KEY, 
                     'rows': 0}

BISON_OCC_FILTERS = {'rows': BISON_MAX_COUNT}


# Common Q Filters
BISON_QFILTERS = {'decimalLatitude': (BISON_BBOX[0], BISON_BBOX[2]),
                   'decimalLongitude': (BISON_BBOX[1], BISON_BBOX[3]),
                   'basisOfRecord': [(False, 'living'), (False, 'fossil')]}
# Common Other Filters
BISON_FILTERS = {'wt': 'json', 
                 'json.nl': 'arrarr'}

# Expected Response Dictionary Keys
BISON_COUNT_KEYS = ['response', 'numFound']
BISON_RECORD_KEYS = ['response', 'docs']
BISON_TSN_LIST_KEYS = ['facet_counts', 'facet_fields', BISON_TSN_KEY]

ITIS_DATA_NAMESPACE = 'http://data.itis_service.itis.usgs.gov/xsd'
# Basic Web Services
ITIS_TAXONOMY_HIERARCHY_URL = 'http://www.itis.gov/ITISWebService/services/ITISService/getFullHierarchyFromTSN'
# JSON Web Services
# ITIS_TAXONOMY_HIERARCHY_URL = 'http://www.itis.gov/ITISService/jsonservice/getFullHierarchyFromTSN'
ITIS_TAXONOMY_KEY = 'tsn'
ITIS_HIERARCHY_TAG = 'hierarchyList'
ITIS_RANK_TAG = 'rankName'
ITIS_TAXON_TAG = 'taxonName'
ITIS_KINGDOM_KEY = 'Kingdom'
ITIS_PHYLUM_DIVISION_KEY = 'Division'
ITIS_CLASS_KEY = 'Class'
ITIS_ORDER_KEY = 'Order'
ITIS_FAMILY_KEY = 'Family'
ITIS_GENUS_KEY = 'Genus'
ITIS_SPECIES_KEY = 'Species'


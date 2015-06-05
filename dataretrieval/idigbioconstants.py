
# .............................................................................
# .                           General constants                               .
# .............................................................................
URL_ESCAPES = [ [" ", "%20"] ]
BINOMIAL_REGEX = "(^[^ ]*) ([^ ]*)$"
INVALIDSP_REGEX = ["sp[.?0-9]*$", "[(]*indet[).?]*$", "[?]$", "l[.]*$"]

# .............................................................................
# .                           iDigBio constants                               .
# .............................................................................
IDIGBIO_SEARCH_URL_PREFIX = 'http://search.idigbio.org/idigbio/records/_search'
IDIGBIO_PUBLISHERS_SEARCH_URL_PREFIX="http://search.idigbio.org/idigbio/publishers/_search"
IDIGBIO_RECORDSETS_SEARCH_URL_PREFIX="http://search.idigbio.org/idigbio/recordsets/_search"
# Query to aggregate all georeferenced binomial scientific names with minimun number (40) of occurrences
IDIGBIO_AGG_SPECIES_GEO_MIN_40 = '{"query":{"filtered":{"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}},{"regexp":{"scientificname":"[^]*[^?]*"}}]},"query":{"bool":{"must_not":[{"term":{"lat":"0"}},{"term":{"lon":"0"}}]}}}},"size":0,"aggregations":{"my_agg":{"terms":{"field":"scientificname","min_doc_count":40,"size":1000000}}}}'
# Deprecated query to aggregate all georeferenced scientific names with minimun number (40) of occurrences
#IDIGBIO_AGG_SPECIES_GEO_MIN_40 = '{"query":{"bool":{"must_not":[{"term":{"lat":"0"}},{"term":{"lon":"0"}}]}},"size":0,"aggregations":{"my_agg":{"terms":{"field":"scientificname","min_doc_count":40,"size":100000}}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]}}'
# Query to retrieve all specimens with a specific scientific name prefix that are georeferenced, including institution and collection codes
IDIGBIO_SPECIMENS_BY_BINOMIAL = '{"query":{"prefix":{"scientificname":"__BINOMIAL__"}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]},"fields":["uuid","scientificname","geopoint.lat","geopoint.lon"],"_source":["data.idigbio:data.dwc:institutionCode","data.idigbio:data.dwc:collectionCode"],"size":1000000,"aggregations":{"filtered_agg":{"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]},"aggregations":{"my_agg":{"terms":{"field":"recordset","min_doc_count":1,"size":10000}}}}}}'
# Deprecated Query to retrieve all specimens with a specific scientific name prefix that are georeferenced, including institution and collection codes
#IDIGBIO_SPECIMENS_BY_BINOMIAL = '{"query":{"prefix":{"scientificname":"__BINOMIAL__"}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]},"fields":["uuid","scientificname","geopoint.lat","geopoint.lon"],_source:["data.idigbio:data.dwc:institutionCode","data.idigbio:data.dwc:collectionCode"],"size":1000000,"aggregations":{"my_agg":{"terms":{"field":"recordset","min_doc_count":1,"size":10000}}}}'
# Deprecated Query to retrieve all specimens with a specific scientific name prefix that are georeferenced, without institution and collection codes
#IDIGBIO_SPECIMENS_BY_BINOMIAL = '{"query":{"prefix":{"scientificname":"__BINOMIAL__"}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]},"fields":["uuid","scientificname","geopoint.lat","geopoint.lon"],"size":1000000,"aggregations":{"my_agg":{"terms":{"field":"recordset","min_doc_count":1,"size":10000}}}}'
# Query to retrieve all ingested recordsets
IDIGBIO_RECORSETS = '{"query":{"query_string":{"default_field":"ingest","query":"true"}},"size": 10000}'
# Query to retrieve the first 10k entries of a certain type
IDIGBIO_FIRST_10K = '{"size": 10000}' 
IDIGBIO_QFILTERS = {}
IDIGBIO_FILTERS = {}

# .............................................................................
# .                              Time constants                               .
# .............................................................................
# Time constants in Modified Julian Day (MJD) units 
ONE_MONTH = 1.0 * 30
ONE_DAY = 1.0
ONE_HOUR = 1.0/24.0
ONE_MIN = 1.0/1440.0
ONE_SEC = 1.0/86400.0


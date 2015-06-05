# These are the WMS parameters that will be used to create the map image

WMS_PARAMETERS = {
   'height' : '400', # Height in pixels of resulting image
   'width' : '800', # Width in pixels of resulting image
   'request' : 'GetMap', # Tells the service to return a map
   'service' : 'WMS',  # Tells the endpoint that this is a WMS request
   'bbox' : '-180.0,-90.0,180.0,90.0', # The bounding box, in decimal degrees, for the resulting image.
                                        #    Format: (min x, min y, max x, max y)
   'srs' : 'epsg:4326', # This is the EPSG code of the resulting map (I don't know if we support anything else)
   'format' : 'image/png', # The MIME type of the resulting image
   'color' : 'red', # The color ramp for the resulting image (Can't be changed currently)
   'version' : '1.1.0', # The WMS version number
   'styles' : ''
}

# Flag indicating if the blue marble background should be included in the projection WMS requests
INCLUDE_BACKGROUND_IMAGE = True


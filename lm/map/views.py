from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from species.models import Species
from constants import *

import os
#os.environ['LIFEMAPPER_CONFIG_FILE'] = '/opt/LmClient/example-config.ini'
os.environ['LIFEMAPPER_CONFIG_FILE'] = '/opt/LmClient/idigbio-config.ini'
from LmClient.lmClientLib import LMClient

def index(request):
    species_list = Species.objects.order_by('species')
    context = {'species_list': species_list,}
    return render(request, 'lm/index.html', context)
#    return HttpResponse("Choose a species:")

def detail(request, species):
    species_list = Species.objects.order_by('species')
    cl = LMClient()
    print species
    expAtoms = cl.sdm.listExperiments(displayName=species)
    expId = expAtoms[0].id # Get only the first experiment id
    exp = cl.sdm.getExperiment(expId)
    algorithmCode = exp.algorithm.code

    # Get the algorithm parameters used to build the model.  Remove items that start with an 
    #    underscore as they are just extra object data that can be ignored
    algorithmParameters = [(n, v) for n,v in exp.algorithm.parameters.__dict__.items() if not n.startswith('_')]
    # Build the main mapping URL parameters (in constants.py)
    urlParams = '&'.join(["%s=%s" % (param, val) for param, val in WMS_PARAMETERS.items()])
    occMapUrl = "%s&%s" % (cl.sdm.getOgcEndpoint(exp.model.occurrenceSet), urlParams)
    if INCLUDE_BACKGROUND_IMAGE:
        occMapUrl = occMapUrl.replace('layers=', 'layers=bmng,')

    # Model summary statement.  I am using a list comprehension to join the algorithm parameters
    modelSummary = ["Experiment " + exp.id + ". Model built with algorithm: " + algorithmCode + ". Occurrences used for the model displayed on the map.", "Parameters: " + ', '.join(["%s = %s" % (p, v) for p, v in algorithmParameters]), occMapUrl]

    #List of projection summaries
    prjsSummary = [None] * len(exp.projections)
    prjOrder = ['WC-5MIN', 'RCP8.5-CCSM4-2050', 'RCP8.5-CCSM4-2070']

    # Build a projection summary tuple for each projection in the experiment
    scenarios = {'RCP8.5-CCSM4-2050': 'Predicted 2041-2060 climate calculated from change modeled by Community Climate System Model, 4.0, National Center for Atmospheric Research (NCAR) for the IPCC Fifth Assessment Report (2013), Family RCP8.5 plus Worldclim 1.4 observed mean climate','RCP8.5-CCSM4-2070': 'Predicted 2061-2080 climate calculated from change modeled by Community Climate System Model, 4.0, National Center for Atmospheric Research (NCAR) for the IPCC Fifth Assessment Report (2013), Family RCP8.5 plus Worldclim 1.4 observed mean climate','WC-5MIN':'WorldClim 1.4 elevation and bioclimatic variables computed from interpolated observation data collected between 1950 and 2000 (http ://www.worldclim.org/), 5 min resolution'}
    for prj in exp.projections:
        mapUrl = "%s&%s" % (cl.sdm.getOgcEndpoint(prj), urlParams)

        if INCLUDE_BACKGROUND_IMAGE:
            mapUrl = mapUrl.replace('layers=', 'layers=bmng,')
        prjsSummary[prjOrder.index(prj.scenarioCode)] = (prj.id, prj.scenarioCode, scenarios[prj.scenarioCode], mapUrl, prj.status) 
        #prjsSummary.append((prj.id, prj.scenarioCode, scenarios[prj.scenarioCode], mapUrl))

    #lyrs = cl.sdm.listProjections(public=True, displayName=species)
    #print "Number of projections:", len(lyrs)
    #maps = []
    #for item in lyrs:
    #    print item.id, item.title
    #    prj = cl.sdm.getProjection(item.id)
    #    u = cl.sdm.getOgcEndpoint(prj)
    #    maps.append(u)
    #    print u

    context = {'species_list': species_list, 'species': species, 'maps': prjsSummary, 'model': modelSummary}
    return render(request, 'lm/index.html', context)

def tutorial(request):
    cl = LMClient()
    scenarios = [ ['RCP8.5-CCSM4-2050', 'Predicted 2041-2060 climate calculated from change modeled by Community Climate System Model, 4.0, National Center for Atmospheric Research (NCAR) for the IPCC Fifth Assessment Report (2013), Family RCP8.5 plus Worldclim 1.4 observed mean climate'],['RCP8.5-CCSM4-2070', 'Predicted 2061-2080 climate calculated from change modeled by Community Climate System Model, 4.0, National Center for Atmospheric Research (NCAR) for the IPCC Fifth Assessment Report (2013), Family RCP8.5 plus Worldclim 1.4 observed mean climate'],['WC-5MIN','WorldClim 1.4 elevation and bioclimatic variables computed from interpolated observation data collected between 1950 and 2000 (http ://www.worldclim.org/), 5 min resolution'] ]
    context = {'scenarios': scenarios}
    return render(request, 'lm/tutorial.html', context)


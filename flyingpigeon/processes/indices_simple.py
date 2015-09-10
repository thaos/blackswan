from malleefowl.process import WPSProcess

from malleefowl import wpslogging as logging
logger = logging.getLogger(__name__)

from flyingpigeon.indices_simple import indices, indices_description, calc_indice_simple
from flyingpigeon.subset import countries, countries_longname
from flyingpigeon.utils import GROUPING

class CalcIndice(WPSProcess):
    """This process calculates a climate indice for the given input netcdf files."""
    def __init__(self):
        WPSProcess.__init__(
            self, 
            identifier = "simple_indice",
            title="Calculation of climate indice (simple)",
            version = "0.1",
            metadata=[],
            abstract="This process calculates a climate indice for the given input netcdf files."
            )

        self.resource = self.addComplexInput(
            identifier="resource",
            title="Resouce",
            abstract="NetCDF File",
            minOccurs=1,
            maxOccurs=100,
            maxmegabites=5000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )
    
        self.grouping = self.addLiteralInput(
            identifier="grouping",
            title="Grouping",
            abstract="Select an aggregation grouping",
            default='year',
            type=type(''),
            minOccurs=1,
            maxOccurs=len(GROUPING),
            allowedValues=GROUPING
            )

        self.indice = self.addLiteralInput(
            identifier="indice",
            title="Indice",
            abstract=indices_description(),
            default='SU',
            type=type(''),
            minOccurs=1,
            maxOccurs=len(indices()),
            allowedValues=indices()
            )
        
        self.region = self.addLiteralInput(
            identifier="region",
            title="Region",
            abstract=countries_longname(),
            default='FRA',
            type=type(''),
            minOccurs=1,
            maxOccurs=len(countries()),
            allowedValues=countries() 
             )
      
        # complex output
        # -------------
        self.output = self.addComplexOutput(
            identifier="output",
            title="Indice",
            abstract="Calculated indice as NetCDF file",
            metadata=[],
            formats=[{"mimeType":"application/x-netcdf"}],
            asReference=True
            )

        # self.drs_filename = self.addLiteralOutput(
        #     identifier = "drs_filename",
        #     title = "DRS Filename",
        #     type = type(''))
        
    def execute(self):
        
        import os
        logger.debug('PYHONPATH = %s', os.environ['PYTHONPATH'])
        logger.debug('PATH = %s', os.environ['PATH'])

        ncs = self.getInputValues(identifier='resource')
        self.show_status('starting: indice=%s, grouping=%s, num_files=%s' % (self.indice.getValue(), self.grouping.getValue(), len(ncs)), 0)

        results = calc_indice_simple(
            resource = ncs,
            indice = self.indice.getValue(),
            grouping = self.grouping.getValue(),
            out_dir = self.working_dir,
            )
        
        self.show_status('result %s' % result, 90)

        self.output.setValue( results )        

        # from os.path import basename
        # for result in results: 
        #     self.drs_filename.setValue( basename(result) )

        self.show_status('done: indice=%s, num_files=%s' % (self.indice.getValue(), len(ncs)), 100)


# from malleefowl.process import WPSProcess
# from malleefowl import wpslogging as logging
# logger = logging.getLogger(__name__)

# #from flyingpigeon.clipping import REGION_EUROPE

# from flyingpigeon.subset import countries, countries_longname
# from flyingpigeon.indices import indices, indice_description
# from flyingpigeon.workflow import calc_indice
# from flyingpigeon.utils import GROUPING

# class CalcMultipleIndices(WPSProcess):
#     def __init__(self):
#         WPSProcess.__init__(
#             self, 
#             identifier = "indices_simple",
#             title="Climate indices based on one input variable",
#             version = "1.0",
#             metadata=[],
#             abstract="This process calculates multiple climate indices for given input netcdf files with the option of polygon subset."
#             )

#         indice_list = indices()
#         self.resource = self.addComplexInput(
#             identifier="resource",
#             title="Resouce",
#             abstract="NetCDF File",
#             minOccurs=1,
#             maxOccurs=1024,
#             maxmegabites=5000,
#             formats=[{"mimeType":"application/x-netcdf"}],
#             )

#         indices_abstract = ['%s : %s'% (indice, indice_description(indice)) for indice in indices()]  
#         self.indices = self.addLiteralInput(
#             identifier="indices",
#             title="Indices",
#             abstract= '\n'.join(indices_abstract),# 'indices',  #'indices', # indices_description(), 
#             default='SU',
#             type=type(''),
#             minOccurs=1,
#             maxOccurs=len(indices()),
#             allowedValues=indices()
#             )

#         self.groupings = self.addLiteralInput(
#             identifier="groupings",
#             title="Time Aggregations",
#             abstract="Select time aggegations",
#             default='yr',
#             type=type(''),
#             minOccurs=1,
#             maxOccurs=len(GROUPING),
#             allowedValues=GROUPING # ["year", "month", "sem"]
#             )

#         #countries_abstract =  countries_longname()
#         self.polygons = self.addLiteralInput(
#             identifier="polygons",
#             title="Polygons",
#             abstract="Select a country for polygon subset" , # countries_abstract, #  '\n'.join(countries_abstract),  # , #countries_longname
#             default='FRA',
#             type=type(''),
#             minOccurs=1,
#             maxOccurs=len(countries()),
#             allowedValues=countries() #REGION_EUROPE #COUNTRIES # 
#             )

#         # complex output
#         # -------------
#         self.output = self.addComplexOutput(
#             identifier="output",
#             title="Indices",
#             abstract="List of calculated indices.",
#             metadata=[],
#             formats=[{"mimeType":"text/json"}],
#             asReference=True
#             )
        
#         self.status_log = self.addComplexOutput(
#             identifier="status_log",
#             title="Status Logfile",
#             abstract="Status of processed files.",
#             metadata=[],
#             formats=[{"mimeType":"text/text"}],
#             asReference=True
#             )
        
        
#         self.out_indices = self.addComplexOutput(
#             title="out_indices",
#             abstract="Tar archive containing the netCDF indices files ",
#             formats=[{"mimeType":"application/x-tar"}],
#             asReference=True,
#             identifier="out_indices",
#             )
        
#     def execute(self):
        
#         ncs = self.getInputValues(identifier='resource')
#         polygons_list = self.getInputValues(identifier='polygons')
#         groupings_list = self.getInputValues(identifier='groupings')

#         my_indices = []
#         indice_list = indices()
#         for indice in indice_list:
#             if self.getInputValue(identifier=indice) == True:
#                 my_indices.append(indice)

#         self.show_status('starting: indice=%s, num_files=%s' % (my_indices, len(ncs)), 0)

#         from os.path import join
#         results = calc_indice(
#             resource = ncs,
#             indices = my_indices,
#             grouping = grouping_list,  # self.grouping.getValue(),
#             out_dir = self.working_dir,
#             status_log = join(self.working_dir, 'status.log'),
#             monitor=self.show_status,
#             )

#         self.show_status("publishing results ...", 99)
        
#         files = [result.strip() for result in results]

#         from malleefowl.publish import publish
#         urls = publish(files)

#         import json
#         outfile = self.mktempfile(suffix='.txt')
#         with open(outfile, 'w') as fp:
#             json.dump(obj=urls, fp=fp, indent=4, sort_keys=True)
#             self.output.setValue(outfile)

#         self.status_log.setValue('status.log')
        
#         self.show_status('done: indice=%s, num_files=%s' % (indice_list, len(ncs)), 100)


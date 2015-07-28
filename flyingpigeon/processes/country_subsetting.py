from malleefowl.process import WPSProcess

from malleefowl import wpslogging as logging
logger = logging.getLogger(__name__)

from flyingpigeon.clipping import REGION_EUROPE, calc_region_clipping
from flyingpigeon.subsetting import countries, countries_longname # COUNTRIES

class SimpleClipping(WPSProcess):

    def __init__(self):
        WPSProcess.__init__(
            self, 
            identifier = "simple_clipping",
            title="Simple Clipping",
            version = "1.0",
            metadata=[],
            abstract="This process returns only the given region from NetCDF file."
            )

        self.resource = self.addComplexInput(
            identifier="resource",
            title="Resource",
            abstract="NetCDF File",
            minOccurs=1,
            maxOccurs=100,
            maxmegabites=5000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )

        self.region = self.addLiteralInput(
            identifier="region",
            title="Region",
            abstract="Select a country for polygon subsetting", #countries_longname
            default='FRA',
            type=type(''),
            minOccurs=1,
            maxOccurs=1,
            allowedValues=countries() #REGION_EUROPE #COUNTRIES # 
             )
      
        # complex output
        # -------------
        self.output = self.addComplexOutput(
            identifier="output",
            title="Output",
            abstract="NetCDF file of region.",
            metadata=[],
            formats=[{"mimeType":"application/x-netcdf"}],
            asReference=True
            )

    def execute(self):
        resources = self.getInputValues(identifier='resource')

        self.show_status('starting: region=%s, num_files=%s' % (self.region.getValue(), len(resources)), 0)

        result = calc_region_clipping(
            resource = resources[0],
            region = self.region.getValue(),
            out_dir = self.working_dir,
            )
        
        self.output.setValue( result )

        self.show_status('done: region=%s, num_files=%s' % (self.region.getValue(), len(resources)), 100)

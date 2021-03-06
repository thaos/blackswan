from .wps_weatherregimes_reanalyse import WeatherregimesreanalyseProcess
# from .wps_weatherregimes_projection import WeatherregimesprojectionProcess
from .wps_weatherregimes_model import WeatherregimesmodelProcess
from .wps_analogs_reanalyse import AnalogsreanalyseProcess
from .wps_analogs_model import AnalogsmodelProcess
from .wps_analogs_compare import AnalogscompareProcess
from .wps_analogs_re2re import AnalogsRe2ReProcess
from .wps_analogs_viewer import AnalogsviewerProcess
from .wps_analogs_cta import AnalogsreanalyseCTA
from .wps_simple_plot import SimplePlot
from .wps_pythonanattribution import PythonanattributionProcess
from .wps_regrsub import Inter_Sub
from .wps_localdims_rea import LocaldimsReaProcess
from .wps_localdims_mod import LocaldimsModProcess
from .wps_farallnat import FARallnatProcess
processes = [
    WeatherregimesreanalyseProcess(),
    # WeatherregimesprojectionProcess(),
    WeatherregimesmodelProcess(),
    AnalogsreanalyseProcess(),
    AnalogsmodelProcess(),
    AnalogscompareProcess(),
    AnalogsRe2ReProcess(),
    AnalogsviewerProcess(),
    AnalogsreanalyseCTA(),
    SimplePlot(),
    PythonanattributionProcess(),
    Inter_Sub(),
    LocaldimsReaProcess(),
    LocaldimsModProcess(),
    FARallnatProcess(),
]

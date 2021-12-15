import itertools
from typing import List, Dict, Type, Sequence, TYPE_CHECKING

import pandas

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.stage import PipelineStage
from evidently.options import OptionsProvider

if TYPE_CHECKING:
    from evidently.analyzers import Analyzer


class Pipeline:
    _analyzers: List[Type['Analyzer']]
    stages: Sequence[PipelineStage]
    analyzers_results: Dict[Type['Analyzer'], object]
    options_provider: OptionsProvider

    def __init__(self, stages: Sequence[PipelineStage], options: list):
        self.stages = stages
        self.analyzers_results = {}
        self.options_provider = OptionsProvider()
        self._analyzers = list(itertools.chain.from_iterable([stage.analyzers() for stage in stages]))
        for option in options:
            self.options_provider.add(option)

    def get_analyzers(self) -> List[Type['Analyzer']]:
        return self._analyzers

    def execute(self,
                reference_data: pandas.DataFrame,
                current_data: pandas.DataFrame,
                column_mapping: ColumnMapping = None):
        if column_mapping is None:
            column_mapping = ColumnMapping()
        for analyzer in self.get_analyzers():
            instance = analyzer()
            instance.options_provider = self.options_provider
            self.analyzers_results[analyzer] =\
                instance.calculate(reference_data, current_data, column_mapping)
        for stage in self.stages:
            stage.options_provider = self.options_provider
            stage.calculate(reference_data, current_data, column_mapping, self.analyzers_results)

from dataclasses import dataclass
from typing import Dict, Type, Any

import pandas

from evidently import ColumnMapping
from evidently.analyzers import Analyzer
from evidently.pipeline import Pipeline, PipelineStage


class StubPipeline(Pipeline):
    pass


@dataclass
class SimpleOptions:
    field1: str = "123"
    field2: int = 123


class AnotherSimpleOptions:
    field1: str = "321"
    field2: int = 321


class SimplePipelineStage(PipelineStage):
    opts: SimpleOptions
    another_opts: AnotherSimpleOptions

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: ColumnMapping,
                  analyzers_results: Dict[Type[Analyzer], Any]):
        self.opts = self.options_provider.get(SimpleOptions)
        self.another_opts = self.options_provider.get(AnotherSimpleOptions)


def test_pipeline():
    stage = SimplePipelineStage()
    pipeline = StubPipeline(stages=[stage], options=[])
    pipeline.execute(None, None, None)
    assert stage.opts.field1 == "123"
    assert stage.opts.field2 == 123
    assert stage.another_opts.field1 == "321"
    assert stage.another_opts.field2 == 321

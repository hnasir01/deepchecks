from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Any, Tuple

__all__ = ['CheckResult', 'Checkable', 'Check', 'CheckSuite', 'Model', 'Dataset']


class CheckResult:
    value: Any
    display: Dict

    def __init__(self, value, display=None):
        """
        Args:
            value (Any):
            display (Dict): Dictionary with formatters for display. possible
            foramtters are: 'text/html', 'image/png'
        """
        self.value = value
        self.display = display

    def _repr_mimebundle_(self, include, exclude):
        if not self.display:
            return None
        data = self.display
        if include:
            data = {k:v for (k,v) in data.items() if k in include}
        if exclude:
            data = {k:v for (k,v) in data.items() if k not in exclude}
        return data

    def _repr_(self):
        return self.value


class Checkable(ABC):
    @abstractmethod
    def run(self, model=None, train_data=None, validation_data=None) -> CheckResult:
        pass

    @abstractmethod
    def run_and_decide(self, model=None, train_data=None, validation_data=None) -> Tuple[CheckResult, bool]:
        pass


class Check(Checkable):
    """
    Check is a utility class which gives the option to combine a check and a decision function to be used together
    """
    decision_func: Callable
    decision_params: Dict
    check_params: Dict

    def __init__(self, decision_func=None, decision_params=None, **check_params):
        self.decision_func = decision_func
        self.decision_params = decision_params
        self.check_params = check_params

    def run_and_decide(self, model=None, train_data=None, validation_data=None) -> Tuple[CheckResult, bool]:
        result = self.run(model=model, train_data=train_data, validation_data=validation_data)
        if self.decision_func:
            decision = self.decision_func(result, **self.decision_params)
        else:
            decision = True
        return result, decision


class CheckSuite:
    checks: List[Checkable]

    def __init__(self, *checks):
        for check in checks:
            if not isinstance(check, Checkable):
                raise Exception(f'CheckSuite receives only `Checkable` objects but got: {check.__class__.__name__}')
        self.checks = checks

    def run(self, model=None, train_data=None, validation_data=None):
        return [check.run(model=model, train_data=train_data, validation_data=validation_data)
                for check in self.checks]

    def run_and_decide(self, model=None, train_data=None, validation_data=None):
        return [check.run_and_decide(model=model, train_data=train_data, validation_data=validation_data)
                for check in self.checks]



class Dataset:
    pass


class Model(ABC):
    model_obj: Any

    # @abstractmethod
    # def fit(self):
    #     pass

    # @abstractmethod
    # def predict(self):
    #     pass


class ScikitModel(Model):
    pass

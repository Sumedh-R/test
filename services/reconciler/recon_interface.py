from abc import ABC, abstractmethod

class ReconInterface(ABC):

    @abstractmethod
    def reconcile(self, payment):
        pass
from abc import ABC, abstractmethod

class OrchInterface(ABC):

    @abstractmethod
    def perform_recon(self, customer):
        pass
from abc import ABC, abstractmethod

class Section(ABC):
	key: str
	label: str

	@abstractmethod
	def render(self, doc: dict): ...

	@abstractmethod
	def validate(self, doc: dict): ...

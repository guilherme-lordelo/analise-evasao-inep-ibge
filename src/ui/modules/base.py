from abc import ABC, abstractmethod

class ConfigModule(ABC):
	key: str
	label: str

	@abstractmethod
	def render_sidebar(self): ...

	@abstractmethod
	def render_main(self): ...

	@abstractmethod
	def validate(self) -> list[str]: ...

	@abstractmethod
	def save(self): ...

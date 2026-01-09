from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.indent(mapping=2, sequence=4, offset=2)


def load_yaml(path: str):
	with open(path, "r", encoding="utf-8") as f:
		return _yaml.load(f)


def save_yaml(doc, path: str):
	with open(path, "w", encoding="utf-8") as f:
		_yaml.dump(doc, f)

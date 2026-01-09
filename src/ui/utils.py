from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

def load_yaml_doc(path: str):
	with open(path) as f:
		return yaml.load(f)

def save_yaml_doc(doc, path: str):
	with open(path, "w") as f:
		yaml.dump(doc, f)

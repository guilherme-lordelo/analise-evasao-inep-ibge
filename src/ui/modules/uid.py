import uuid

def get_sheet_uid(sheet: dict) -> str:
	"""
	Gera UID apenas para controle de UI.
	Nunca deve ser persistido no YAML.
	"""
	if "_ui_uid" not in sheet:
		sheet["_ui_uid"] = uuid.uuid4().hex
	return sheet["_ui_uid"]

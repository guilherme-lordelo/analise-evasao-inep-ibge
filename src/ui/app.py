import streamlit as st
from ui.state import init_state
from ui.modules.inep import INEPModule
from ui.modules.ibge import IBGEModule


MODULES = [
	INEPModule(),
	IBGEModule(),
]


def main():
	init_state()

	st.set_page_config(
		page_title="Editor de Configurações",
		layout="wide"
	)

	st.title("Editor de Configurações")

	st.sidebar.title("Módulo")

	module_labels = {m.key: m.label for m in MODULES}
	module_keys = list(module_labels.keys())

	if "active_module" not in st.session_state:
		st.session_state.active_module = module_keys[0]

	st.session_state.active_module = st.sidebar.radio(
		"",
		module_keys,
		format_func=module_labels.get
	)

	active = next(
		m for m in MODULES
		if m.key == st.session_state.active_module
	)

	st.sidebar.divider()

	active.render_sidebar()

	active.render_main()

	st.divider()

	col1, col2 = st.columns(2)

	with col1:
		if st.button("Validar configuração"):
			erros = active.validate()
			if erros:
				st.error("Foram encontrados erros:")
				for e in erros:
					st.write(f"• {e}")
			else:
				st.success("Configuração válida")

	with col2:
		if st.button("Salvar arquivo"):
			active.save()
			st.success(f"Arquivo {active.label} salvo")


if __name__ == "__main__":
	main()

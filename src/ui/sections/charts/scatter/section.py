import streamlit as st
from ui.sections.base_section import Section


class ScatterSection(Section):
	key = "scatter"
	label = "Dispersão (Scatter)"

	def render(self, doc: dict):
		cfg = doc.setdefault("scatter", {})
		plot_cfg = cfg.setdefault("plot", {})
		saida_cfg = cfg.setdefault("saida", {})
		plots = cfg.setdefault("plots", [])

		st.subheader("Configurações Gerais")

		figsize = plot_cfg.get("figsize", [6, 6])

		col1, col2 = st.columns(2)
		w = col1.number_input(
			"Largura da figura",
			min_value=1.0,
			step=0.5,
			value=float(figsize[0]),
		)
		h = col2.number_input(
			"Altura da figura",
			min_value=1.0,
			step=0.5,
			value=float(figsize[1]),
		)

		plot_cfg["figsize"] = [w, h]

		plot_cfg["mostrar_titulo"] = st.checkbox(
			"Mostrar título",
			value=plot_cfg.get("mostrar_titulo", True),
		)

		plot_cfg["grid"] = st.checkbox(
			"Mostrar grid",
			value=plot_cfg.get("grid", True),
		)

		st.divider()
		st.subheader("Gráficos")

		for i, p in enumerate(plots):
			with st.expander(p.get("nome", f"Scatter {i+1}"), expanded=False):
				p["nome"] = st.text_input(
					"Nome",
					value=p.get("nome", ""),
					key=f"sc_nome_{i}",
				)

				p["nivel"] = st.selectbox(
					"Nível",
					["nacional", "estadual", "municipal"],
					index=["nacional", "estadual", "municipal"].index(
						p.get("nivel", "nacional")
					),
					key=f"sc_nivel_{i}",
				)

				p["eixo_x"] = st.text_input(
					"Eixo X",
					value=p.get("eixo_x", ""),
					key=f"sc_x_{i}",
				)

				p["eixo_y"] = st.text_input(
					"Eixo Y",
					value=p.get("eixo_y", ""),
					key=f"sc_y_{i}",
				)

		if st.button("Adicionar gráfico de dispersão"):
			plots.append({
				"nome": "",
				"nivel": "nacional",
				"eixo_x": "",
				"eixo_y": "",
			})

		st.divider()
		st.subheader("Saída")

		saida_cfg["formato"] = st.selectbox(
			"Formato",
			["png", "pdf", "svg"],
			index=["png", "pdf", "svg"].index(saida_cfg.get("formato", "png")),
		)

		saida_cfg["dpi"] = st.number_input(
			"DPI",
			min_value=50,
			value=saida_cfg.get("dpi", 150),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("scatter", {})

		figsize = cfg.get("plot", {}).get("figsize")
		if (
			not isinstance(figsize, list)
			or len(figsize) != 2
			or not all(isinstance(v, (int, float)) for v in figsize)
		):
			erros.append("Scatter: figsize inválido (esperado: [largura, altura]).")

		if not cfg.get("plots"):
			erros.append("Scatter: nenhum gráfico configurado.")

		for i, p in enumerate(cfg.get("plots", [])):
			if not p.get("nome"):
				erros.append(f"Scatter [{i+1}]: nome não informado.")
			if not p.get("eixo_x") or not p.get("eixo_y"):
				erros.append(f"Scatter [{i+1}]: eixo X ou Y não informado.")

		return erros

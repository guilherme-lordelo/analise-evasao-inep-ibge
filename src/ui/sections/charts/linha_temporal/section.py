import streamlit as st
from ui.sections.base_section import Section


class LinhaTemporalSection(Section):
	key = "linha_temporal"
	label = "Linha Temporal"

	def render(self, doc: dict):
		cfg = doc.setdefault("linha_temporal", {})
		plot_cfg = cfg.setdefault("plot", {})
		saida_cfg = cfg.setdefault("saida", {})
		plots = cfg.setdefault("plots", [])

		st.subheader("Configurações Gerais")

		figsize = plot_cfg.get("figsize", [8, 4])

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

		plot_cfg["max_variaveis_por_plot"] = st.number_input(
			"Máx. variáveis por gráfico",
			min_value=1,
			value=plot_cfg.get("max_variaveis_por_plot", 4),
		)

		st.divider()
		st.subheader("Gráficos")

		for i, p in enumerate(plots):
			with st.expander(p.get("nome", f"Plot {i+1}"), expanded=False):
				p["nome"] = st.text_input(
					"Nome",
					value=p.get("nome", ""),
					key=f"lt_nome_{i}",
				)

				p["nivel"] = st.selectbox(
					"Nível",
					["nacional", "estadual", "municipal"],
					index=["nacional", "estadual", "municipal"].index(
						p.get("nivel", "nacional")
					),
					key=f"lt_nivel_{i}",
				)

				vars_str = ",".join(p.get("variaveis", []))
				p["variaveis"] = [
					v.strip() for v in st.text_input(
						"Variáveis (separadas por vírgula)",
						value=vars_str,
						key=f"lt_vars_{i}",
					).split(",") if v.strip()
				]

		if st.button("Adicionar gráfico de linha temporal"):
			plots.append({"nome": "", "nivel": "nacional", "variaveis": []})

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
		cfg = doc.get("linha_temporal", {})

		figsize = cfg.get("plot", {}).get("figsize")
		if (
			not isinstance(figsize, list)
			or len(figsize) != 2
			or not all(isinstance(v, (int, float)) for v in figsize)
		):
			erros.append("Linha Temporal: figsize inválido (esperado: [largura, altura]).")

		if not cfg.get("plots"):
			erros.append("Linha Temporal: nenhum gráfico configurado.")

		for i, p in enumerate(cfg.get("plots", [])):
			if not p.get("nome"):
				erros.append(f"Linha Temporal [{i+1}]: nome não informado.")
			if not p.get("variaveis"):
				erros.append(f"Linha Temporal [{i+1}]: nenhuma variável definida.")

		return erros

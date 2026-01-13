import streamlit as st
from ui.sections.base_section import Section


class PlotSection(Section):
	key = "plot"
	label = "Plotagem"

	def render(self, doc: dict):
		cfg = doc.setdefault("plot", {})

		st.subheader("Configurações de Plotagem")

		cfg["cmap"] = st.text_input(
			"Colormap (cmap)",
			value=cfg.get("cmap", "OrRd"),
		)

		cfg["legend_shrink"] = st.number_input(
			"Redução da legenda",
			min_value=0.1,
			max_value=1.0,
			step=0.1,
			value=float(cfg.get("legend_shrink", 0.5)),
		)

		figsize = cfg.get("figsize", [14, 14])

		col1, col2 = st.columns(2)
		w = col1.number_input(
			"Largura da figura",
			min_value=1.0,
			step=1.0,
			value=float(figsize[0]),
		)
		h = col2.number_input(
			"Altura da figura",
			min_value=1.0,
			step=1.0,
			value=float(figsize[1]),
		)

		cfg["figsize"] = [w, h]

		cfg["mostrar_titulo"] = st.checkbox(
			"Mostrar título",
			value=cfg.get("mostrar_titulo", False),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("plot", {})

		figsize = cfg.get("figsize")
		if (
			not isinstance(figsize, list)
			or len(figsize) != 2
			or not all(isinstance(v, (int, float)) for v in figsize)
		):
			erros.append("Mapas/Plot: figsize inválido (esperado: [largura, altura]).")

		if not cfg.get("cmap"):
			erros.append("Mapas/Plot: cmap não informado.")

		return erros

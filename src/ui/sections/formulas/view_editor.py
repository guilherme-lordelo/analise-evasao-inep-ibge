import streamlit as st

def render_editor(formulas: dict, nome: str):
	formula = formulas[nome]

	st.subheader(f"Editando: {nome}")

	if st.button("← Voltar"):
		st.session_state.view = "lista"
		st.session_state.formula_atual = None
		st.rerun()

	formula["descricao"] = st.text_input(
		"Descrição",
		value=formula.get("descricao", ""),
	)

	formula["expressao"] = st.text_area(
		"Expressão",
		value=formula.get("expressao", ""),
		height=100,
	)

	st.markdown("### Regras de validação")

	validacao = formula.setdefault("validacao", {})
	regras = validacao.setdefault("regras", [])

	for i, regra in enumerate(list(regras)):
		col1, col2 = st.columns([8, 1])

		with col1:
			regras[i] = st.text_input(
				f"Regra {i + 1}",
				value=regra,
				key=f"regra_{nome}_{i}",
			)

		with col2:
			if st.button("Remover", key=f"del_{nome}_{i}"):
				regras.pop(i)
				st.rerun()

	if st.button("Adicionar regra"):
		regras.append("")
		st.rerun()

from ruamel.yaml.comments import CommentedSeq

def flow_seq(valores):
	seq = CommentedSeq(valores)
	seq.fa.set_flow_style()
	return seq

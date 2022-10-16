# coding:utf-8
import re
import sys
import copy
import json
import yaml
import penman
from tqdm import tqdm
from pathlib import Path
from IO import read_raw_amr_data


def _tokenize_encoded_graph(encoded):
    linearized = re.sub(r"(\".+?\")", r" \1 ", encoded)
    pieces = []
    for piece in linearized.split():
        if piece.startswith('"') and piece.endswith('"'):
            pieces.append(piece)
        else:
            piece = piece.replace("(", " ( ")
            piece = piece.replace(")", " ) ")
            piece = piece.replace(":", " :")
            piece = piece.replace("/", " / ")
            piece = piece.strip()
            pieces.append(piece)
    linearized = re.sub(r"\s+", " ", " ".join(pieces)).strip()
    return linearized.split(" ")


# def _get_nodes(graph):
#     graph_ = copy.deepcopy(graph)
#     graph_.metadata = {}
#     linearized = penman.encode(graph_)
#     linearized_nodes = _tokenize_encoded_graph(linearized)

#     if use_pointer_tokens:
#         remap = {}
#         for i in range(1, len(linearized_nodes)):
#             nxt = linearized_nodes[i]
#             lst = linearized_nodes[i - 1]
#             if nxt == "/":
#                 remap[lst] = f"<pointer:{len(remap)}>"
#         i = 1
#         linearized_nodes_ = [linearized_nodes[0]]
#         while i < (len(linearized_nodes)):
#             nxt = linearized_nodes[i]
#             lst = linearized_nodes_[-1]
#             if nxt in remap:
#                 if lst == "(" and linearized_nodes[i + 1] == "/":
#                     nxt = remap[nxt]
#                     i += 1
#                 elif lst.startswith(":"):
#                     nxt = remap[nxt]
#             linearized_nodes_.append(nxt)
#             i += 1
#         linearized_nodes = linearized_nodes_
#         if remove_pars:
#             linearized_nodes = [n for n in linearized_nodes if n != "("]
#     return linearized_nodes


def dfs_linearize(graph):
    graph_ = copy.deepcopy(graph)
    graph_.metadata = {}
    linearized = penman.encode(graph_)
    linearized_nodes = _tokenize_encoded_graph(linearized)

    if use_pointer_tokens:
        remap = {}
        for i in range(1, len(linearized_nodes)):
            nxt = linearized_nodes[i]
            lst = linearized_nodes[i - 1]
            if nxt == "/":
                remap[lst] = f"<pointer:{len(remap)}>"
        i = 1
        linearized_nodes_ = [linearized_nodes[0]]
        while i < (len(linearized_nodes)):
            nxt = linearized_nodes[i]
            lst = linearized_nodes_[-1]
            if nxt in remap:
                if lst == "(" and linearized_nodes[i + 1] == "/":
                    nxt = remap[nxt]
                    i += 1
                elif lst.startswith(":"):
                    nxt = remap[nxt]
            linearized_nodes_.append(nxt)
            i += 1
        linearized_nodes = linearized_nodes_
        if remove_pars:
            linearized_nodes = [n for n in linearized_nodes if n != "("]
    return linearized_nodes


if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        description="AMR processing script",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--config', type=Path, default='default.yaml',
        help='Use the following config for hparams.')
    parser.add_argument('--input_file', type=str,
        help='The input AMR file.')
    parser.add_argument('--output_prefix', type=str,
        help='The output_prefix.')
    
    args, unknown = parser.parse_known_args()

    with args.config.open() as y:
        config = yaml.load(y, Loader=yaml.FullLoader)

    remove_pars = False
    use_pointer_tokens = True
    graphs = read_raw_amr_data(
        [args.input_file],
        use_recategorization=config["use_recategorization"],
        remove_wiki=config["remove_wiki"],
        dereify=config["dereify"],
    )

    line_amr, sentences = [], []

    for g in tqdm(graphs):
        lin_tokens = dfs_linearize(g)
        sentences.append(g.metadata["snt"])
        #line_amr.append(" ".join(lin_tokens[1:-1]))
        line_amr.append(" ".join(lin_tokens))

    print(f"all {len(line_amr)} AMRs processed")

    with open(args.output_prefix + ".amr", "w", encoding="utf-8") as fout:
        fout.write("\n".join(line_amr) + "\n")

    with open(args.output_prefix + ".txt", "w", encoding="utf-8") as fout:
        fout.write("\n".join(sentences) + "\n")

    res_out = [json.dumps({"sent": sent, "amr": lamr}) for lamr, sent in zip(line_amr, sentences)]

    with open(args.output_prefix + ".jsonl", "w", encoding="utf-8") as fout:
        fout.write("\n".join(res_out) + "\n")


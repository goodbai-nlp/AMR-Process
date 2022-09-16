# coding:utf-8
# the code is migrated from https://github.com/SapienzaNLP/spring 

import glob
from pathlib import Path
from typing import List, Union, Iterable
from penman_interface import load as pm_load


def read_raw_amr_data(
    paths: List[Union[str, Path]], use_recategorization=False, dereify=True, remove_wiki=False,
):
    """ code for loading AMR from a set of files
        - use_recategorization: use graph recategorization trick
        - dereify: Dereify edges in g that have reifications in model.
        - remove_wiki: remove wiki links
    """
    assert paths
    if not isinstance(paths, Iterable):
        paths = [paths]

    graphs = []
    for path_ in paths:
        for path in glob.glob(str(path_)):
            path = Path(path)
            graphs.extend(pm_load(path, dereify=dereify, remove_wiki=remove_wiki))

    assert graphs

    if use_recategorization:
        for g in graphs:
            metadata = g.metadata
            metadata["snt_orig"] = metadata["snt"]
            tokens = eval(metadata["tokens"])
            metadata["snt"] = " ".join(
                [
                    t
                    for t in tokens
                    if not ((t.startswith("-L") or t.startswith("-R")) and t.endswith("-"))
                ]
            )

    return graphs

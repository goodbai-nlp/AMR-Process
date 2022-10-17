# AMR-Process
Code for preprocessing AMR graphs.

## Graph Operations

- [x] remove wiki
- [x] graph recategorizate
- [ ] anonymize concept sense
- [ ] anonymize Entities

## Graph Transformations

- [x] DFS linearization
- [x] levi graph transformation
- [x] add pointer
- [x] reify_edges
- [x] dereify_edges

## Linerazing AMR graphs (Bai et al., ACL2022)

1. Concatenate splitted AMRs into one file:
```
cat /path/to/amr_files > /path/to/xxx-all.txt
```

2. Move the concatenated file into corresponding directory and run graph linearization script:
```
bash run-process-acl2022.sh
```
The processed files will be in the ``outputs`` directory.

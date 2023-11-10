## Callee Analysis
```bash
perf record -e br_inst_retired.indirect:P -c 10001 -j ind_call -o PATH_OF_PERF_DATA WORKLOAD_CMD
perf report -i PATH_OF_PERF_DATA -F overhead,dso_to,symbol_to
```

## Caller Analysis
Indirect caller analysis

```bash
# collect
perf record -e br_inst_retired.indirect:P -c 10001 -o PATH_OF_PERF_DATA WORKLOAD_CMD
# analysis, sorted by indirect call count
python3 script.py PATH_OF_PERF_DATA
```

### Example

```bash
# compile
clang++ main.cc -o test
perf record -e br_inst_retired.indirect:P -c 10001 -o perf.data.test ./test
python3 script.py perf.data.test
```

Output will be like below:
```bash
Percent, symbol
48.98%, test testA()
29.13%, test testC()
21.89%, test testB()

```


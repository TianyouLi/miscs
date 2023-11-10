all: perf

indicall:
	clang++ -O2 -g -o indicall main.cc

perf: indicall
	perf record -e br_inst_retired.indirect:P -c 10001 -o perf.data.test ./indicall
	python3 script.py perf.data.test
clean:
	rm -f ./indicall perf.data*

import os
import re
import sys


def perf_annotate(perf_data, output_file):
    cmd = ' '.join([
        'perf annotate',
        '--show-total-period --stdio',
        '--ignore-vmlinux --skip-missing',
        '--no-demangle',
        '-i %s' % perf_data,
        '> %s' % output_file,
    ])
    print('Running cmd:', cmd)
    os.system(cmd)


def parse_dso(line):
    regexp = r'Source code & Disassembly of (.*) for'
    m = re.search(regexp, line)
    return m.groups(1)[0]


def parse_sym(line):
    parts = line.split(':')
    return parts[-2].split()[-1]


def analysis_annotate(annotate_file):
    print('Analysis annotation...')
    total_periods = 0
    sym_periods = 0
    symbol_map = {}
    cur_dso = None
    cur_sym = None
    with open(annotate_file) as fp:
        for line in fp.readlines():
            parts = line.split(':')
            prefix = parts[0].strip()
            if prefix.startswith('Period'):
                cur_dso = parse_dso(line)
            elif prefix.isdigit():
                asm = parts[2].strip()
                if asm.startswith('call'):  # valid call
                    period = int(prefix)
                    total_periods += period
                    sym_periods += period
            elif len(parts) > 2 and parts[-2].endswith('()'):
                # new sym, first save
                if cur_sym is not None:
                    key = cur_dso + ' ' + cur_sym
                    symbol_map[key] = sym_periods
                    sym_periods = 0
                cur_sym = parse_sym(line)
        # handle for last sym
        key = cur_dso + ' ' + cur_sym
        symbol_map[key] = sym_periods
    # report
    pairs = sorted(symbol_map.items(), key=lambda it: it[1], reverse=True)
    print("Percent, symbol")
    for p in pairs:
        print('%2.2f%%, %s' % (p[1]*100/float(total_periods), p[0]))


if __name__ == "__main__":
    perf_data = sys.argv[-1]
    annotate_file = perf_data + '.annonate'
    perf_annotate(perf_data, annotate_file)
    analysis_annotate(annotate_file)

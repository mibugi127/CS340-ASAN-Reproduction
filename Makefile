CC = clang
CFLAGS = -O2 -fsanitize=address -fno-omit-frame-pointer -g
CFLAGS_BASE = -O2 -g

EXP_DIR = experiments
BUILD_DIR = build

BUGS_SRCS = $(wildcard $(EXP_DIR)/bugs/*.c)
PERF_SRCS = $(wildcard $(EXP_DIR)/perf/*.c)
STACK_SRC = $(EXP_DIR)/perf/stack_probe.c

BUGS_BINS = $(patsubst $(EXP_DIR)/bugs/%.c, $(BUILD_DIR)/bugs/%, $(BUGS_SRCS))
PERF_BINS = $(patsubst $(EXP_DIR)/perf/%.c, $(BUILD_DIR)/perf/%, $(PERF_SRCS))
STACK_BIN = $(BUILD_DIR)/perf/stack_probe

all: dirs $(BUGS_BINS) $(PERF_BINS) $(STACK_BIN)

base: dirs
	@mkdir -p $(BUILD_DIR)/perf_base
	@for f in $(PERF_SRCS); do \
		n=$$(basename $$f .c); \
		$(CC) $(CFLAGS_BASE) $$f -o $(BUILD_DIR)/perf_base/$${n}_base; \
	done

dirs:
	@mkdir -p $(BUILD_DIR)/bugs
	@mkdir -p $(BUILD_DIR)/perf

$(BUILD_DIR)/bugs/%: $(EXP_DIR)/bugs/%.c
	$(CC) $(CFLAGS) $< -o $@

$(BUILD_DIR)/perf/%: $(EXP_DIR)/perf/%.c
	$(CC) $(CFLAGS) $< -o $@

$(STACK_BIN): $(STACK_SRC)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all dirs base clean
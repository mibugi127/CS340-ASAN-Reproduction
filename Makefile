CC = clang

CFLAGS = -O2 -fsanitize=address -fno-omit-frame-pointer -g

EXP_DIR = experiments
BUILD_DIR = build

BUGS_SRCS = $(wildcard $(EXP_DIR)/bugs/*.c)
PERF_SRCS = $(wildcard $(EXP_DIR)/perf/*.c)
STACK_SRC = $(EXP_DIR)/perf/stack_probe.c

BUGS_BINS = $(patsubst $(EXP_DIR)/bugs/%.c, $(BUILD_DIR)/bugs/%, $(BUGS_SRCS))
PERF_BINS = $(patsubst $(EXP_DIR)/perf/%.c, $(BUILD_DIR)/perf/%, $(PERF_SRCS))
STACK_BIN = $(BUILD_DIR)/stack_probe

all: dirs $(BUGS_BINS) $(PERF_BINS) $(STACK_BIN)

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

.PHONY: all dirs clean
# ==============================================================================
# IAGROK NATIVE C99 ENGINE - MAKEFILE
# 100% ANSI C99 / AVX2 / Win32 - Zero Python Runtime
# ==============================================================================

CC = gcc
CFLAGS = -std=c99 -O2 -Wall -Wextra -mavx2 -mfma -I.
LDFLAGS = -lws2_32 -lpsapi -lwininet -lm

TARGET = iagrok_server.exe

SRCS = iagrok_hardware.c \
       iagrok_simd.c \
       iagrok_embed.c \
       iagrok_triad.c \
       iagrok_fs.c \
       iagrok_chat.c \
       iagrok_http.c \
       iagrok_ops.c \
       iagrok_agent.c \
       iagrok_shield.c \
       iagrok_neurobus.c \
       iagrok_boveda.c \
       iagrok_main.c

OBJS = $(SRCS:.c=.o)

.PHONY: all clean test bench triad

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)
	@echo [OK] Built $(TARGET) successfully.

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

test: $(TARGET)
	./$(TARGET) --test

bench: $(TARGET)
	./$(TARGET) --bench-simd 100000 1536

triad: $(TARGET)
	./$(TARGET) --triad

clean:
	rm -f $(OBJS) $(TARGET)

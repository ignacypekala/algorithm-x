CC = gcc
CFLAGS = @options

.PHONY: all clean

all: algorithm_x

algorithm_x: algorithm_x.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm algorithm_x

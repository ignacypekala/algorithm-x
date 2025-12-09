CC = gcc
CLFAGS = @options

.PHONY: all clean

all: algorithm_x

algorithm_x: algorithm_x.c
	$(CC) $(CLFAGS) -o $@ $<

clean:
	rm algorithm_x

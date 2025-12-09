/*
 * Algorithm X program, solving the exact cover problem.
 * For a given filter of length n consisting of +/- characters and an m x n matrix consisting of characters, 
 * it prints a list of words obtainable by creating combinations of matrix rows that ensure an exact cover of the set.
 * The output words pass through a filter that removes characters at positions with a minus sign in the filter.
 *
 * Sample input:
 * + + -
 * A _ B
 * _ C _
 * D E _
 *
 * Output:
 * AC
 *
 * Author: Ignacy Pękała
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

// Constants defining the initial number of columns/rows we allocate.
#define DEFAULT_COLUMN_COUNT 5
#define DEFAULT_ROW_COUNT 10

#define MAX_COLUMN_COUNT 300
#define MAX_ROW_COUNT 200

// Helper functions
int min(int a, int b) { return (a < b) ? a : b; }

// Reading input
/*
 * Allocation strategy:
 * We start by allocating space for a matrix of a small size. If we encounter data exceeding the
 * currently allocated space, we reallocate to the smaller of:
 * * twice the current space
 * * the maximum allowed input size
 *
 * We apply this strategy for both columns and rows.
 */
char current_char;
char read_char() {
    current_char = (char) getchar();
    return current_char;
}

// Reads the filter from the input, saving it to the provided character array pointer.
int read_filter(char ** filter) {
    assert(*filter == NULL);
    int columns = 0, allocated_columns = DEFAULT_COLUMN_COUNT;
    *filter = (char *) malloc(sizeof(char *) * (size_t) allocated_columns);

    while (read_char() != '\n' && current_char != EOF) {
        columns++;
        if (columns > allocated_columns) {
            allocated_columns = min(allocated_columns * 2, MAX_COLUMN_COUNT);
            *filter = (char *) realloc(*filter, sizeof(char *) * (size_t) allocated_columns);
        }
        (*filter)[columns - 1] = current_char;
    }

    return columns;
}

// Reads the matrix and saves it to the provided pointer to an array of character arrays.
int read_matrix(char ***matrix, int columns) {
    assert(*matrix == NULL);
    int allocated_rows = DEFAULT_ROW_COUNT;
    *matrix = (char **) malloc(sizeof(char **) * (size_t) allocated_rows);
    char *row = malloc(sizeof(char *) * (size_t) columns);
    int rows = 0;

    int i = 0;
    while (read_char() != EOF) {
        // If we find the end of a line after reading the appropriate number of characters,
        // we save the row to the matrix. Otherwise, we append the character to the current row.
        if (current_char == '\n' && i == columns) {
            rows++;
            if (rows > allocated_rows) {
                allocated_rows = min(allocated_rows * 2, MAX_ROW_COUNT);
                *matrix = (char **) realloc(*matrix, sizeof(char **) * (size_t) allocated_rows);
            }

            (*matrix)[rows - 1] = row;
            row = malloc(sizeof(char) * (size_t) columns);
            i = 0;
        } else {
            row[i] = current_char;
            i++;
        }
    }
    free(row);
    return rows;
}


// Prints the specified row, taking the given filter into account.
void print_row(const char *row, const char *filter, int n) {
    for (int i = 0; i < n; i++) {
        if (filter[i] == '+') putchar(row[i]);
    }
    putchar('\n');
}

/*
 * Function implementing the recursive solution to the problem.
 * Through successive calls, we explore further combinations of sets. If we find an exact cover, 
 * we exit and print the formed word.
 */
void solve(
        char **matrix, // Input matrix
        char *filter, // Input filter
        char *row, // Array where we write the currently formed combination of rows.
        const int rows, // Number of rows
        const int columns, // Number of columns
        const int start_row // Row index from which we will start searching for subsequent ones
        ) {
    // Count the empty characters
    int empty_count = 0;
    for (int i = 0; i < columns; i++) empty_count += row[i] == '_' ? 1 : 0;

    // Exit if we have found an exact cover
    if (empty_count == 0) {
        print_row(row, filter, columns);
        return;
    }

    for (int i = start_row; i < rows; i++) {
        // Check if the i-th row is disjoint with the current combination.
        bool is_disjoint = true;
        int j = 0;
        while (is_disjoint && j < columns) {
            if (row[j] != '_' && matrix[i][j] != '_') {
                is_disjoint = false;
            }
            j++;
        }

        if (is_disjoint) {
            // Add it to the combination.
            for (j = 0; j < columns; j++) {
                if (matrix[i][j] != '_') row[j] = matrix[i][j];
            }

            solve(matrix, filter, row, rows, columns, i + 1);

            // Remove it from the combination.
            for (j = 0; j < columns; j++) {
                if (matrix[i][j] != '_') row[j] = '_';
            }
        }
    }
}

int main() {
    char *filter = NULL;
    int columns = read_filter(&filter);

    char **matrix = NULL;
    int rows = read_matrix(&matrix, columns);

    // Working memory for the recursive `solve` function
    char *row = malloc(sizeof(char) * (size_t) columns);
    for (int i = 0; i < columns; i++) row[i] = '_';

    solve(matrix, filter, row, rows, columns, 0);

    // Cleanup
    free(row);
    free(filter);
    for (int i = 0; i < rows; i++) free(matrix[i]);
    free(matrix);
    return 0;
}

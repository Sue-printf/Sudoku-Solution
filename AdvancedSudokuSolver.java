import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class AdvancedSudokuSolver {

    private static final int EMPTY_CELL = 0;

    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader("sudoku_boards.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                int[][] board = sudokuStringToBoard(line);
                if (solveSudoku(board)) {
                    printBoard(board);
                } else {
                    System.out.println("No solution exists.");
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }

    private static int[][] sudokuStringToBoard(String sudokuString) {
        int[][] board = new int[9][9];
        for (int i = 0; i < 81; i++) {
            int row = i / 9;
            int col = i % 9;
            board[row][col] = sudokuString.charAt(i) - '0';
        }
        return board;
    }

    private static boolean solveSudoku(int[][] board) {
        int row = findEmptyCell(board);
        if (row == -1) {
            return true; // Board is already solved
        }
        int col = findEmptyCell(board, row);
        for (int num = 1; num <= 9; num++) {
            if (isValid(board, row, col, num)) {
                board[row][col] = num;
                if (solveSudoku(board)) {
                    return true;
                }
                board[row][col] = EMPTY_CELL; // Backtrack
            }
        }
        return false; // No valid number can be placed in this cell
    }

    private static int findEmptyCell(int[][] board) {
        for (int row = 0; row < 9; row++) {
            for (int col = 0; col < 9; col++) {
                if (board[row][col] == EMPTY_CELL) {
                    return row;
                }
            }
        }
        return -1; // No empty cell found
    }

    private static int findEmptyCell(int[][] board, int row) {
        for (int col = 0; col < 9; col++) {
            if (board[row][col] == EMPTY_CELL) {
                return col;
            }
        }
        return -1; // No empty cell found in the specified row
    }

    private static boolean isValid(int[][] board, int row, int col, int num) {
        for (int x = 0; x < 9; x++) {
            if (board[row][x] == num || board[x][col] == num) {
                return false;
            }
        }
        int boxRowStart = row - row % 3;
        int boxColStart = col - col % 3;
        for (int i = boxRowStart; i < boxRowStart + 3; i++) {
            for (int j = boxColStart; j < boxColStart + 3; j++) {
                if (board[i][j] == num) {
                    return false;
                }
            }
        }
        return true;
    }

    private static void printBoard(int[][] board) {
    for (int i = 0; i < 9; i++) {
        if (i % 3 == 0 && i != 0) // not first iteration
            System.out.println(); // print extra new-line each 3 iterations

        for (int j = 0; j < 9; j++) {
            if (j % 3 == 0) 
                System.out.print(" "); // to print spaces between columns

            System.out.print(board[i][j] + " ");
        }
        System.out.println();
    }
}
}

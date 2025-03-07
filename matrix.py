def find_all_paths_in_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    all_paths = []
    
    # All possible directions: up, down, left, right, and four diagonals
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    
    target_row = 2  # Zero-based index (Row 2)

    def backtrack(path, row, col, visited):
        # Add the current cell to the path and mark it as visited
        path.append((row, col))
        visited.add((row, col))
        print(f"Exploring cell ({row}, {col}), Current path: {path}")
        
        if row == target_row:
            # Allow movements within the target row
            can_move_within_row = False
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                # Only allow horizontal or diagonal movements within the same row
                if next_row == row:
                    if (0 <= next_col < cols and
                        matrix[next_row][next_col] == 0 and
                        (next_row, next_col) not in visited):
                        can_move_within_row = True
                        backtrack(path, next_row, next_col, visited)
            if not can_move_within_row:
                # No further moves within the target row; append the path
                print(f"Reached target row and no further moves from ({row}, {col}), Path complete: {path}")
                all_paths.append(path.copy())
        else:
            # Allow all directions if not yet in the target row
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if (0 <= next_row < rows and
                    0 <= next_col < cols and
                    matrix[next_row][next_col] == 0 and
                    (next_row, next_col) not in visited):
                    backtrack(path, next_row, next_col, visited)
        
        # Backtrack by removing the current cell from the path and visited set
        path.pop()
        visited.remove((row, col))

    # Start from all possible `0`s in the first row
    for col in range(cols):
        if matrix[0][col] == 0:
            backtrack([], 0, col, set())
    
    return all_paths

# Example Matrix
matrix = [
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [0, 0, 0, 0],
    [1, 1, 1, 1]  # No `0` here; traversal will stop
]

result = find_all_paths_in_matrix(matrix)
if result:
    print("\nAll valid paths:")
    for path in result:
        print("path",path)
else:
    print("No valid paths found.")
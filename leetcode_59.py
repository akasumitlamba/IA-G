class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        # Initialize the result matrix
        res = [[0] * n for _ in range(n)]
        
        # Initialize directions for right, down, left, and up movements
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x, y = 0, 0  # Starting position
        dx, dy = directions[0]  # Start with the "right" direction
        
        for i in range(1, n * n + 1):
            res[x][y] = i  # Place the current number
            
            # Calculate the next position
            nx, ny = x + dx, y + dy
            
            # Check if the next position is out of bounds or already filled
            if not (0 <= nx < n and 0 <= ny < n and res[nx][ny] == 0):
                # Change direction: (right -> down -> left -> up)
                dx, dy = directions[(directions.index((dx, dy)) + 1) % 4]
                nx, ny = x + dx, y + dy
            
            # Move to the next position
            x, y = nx, ny
        
        return res

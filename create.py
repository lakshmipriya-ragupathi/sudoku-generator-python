from random import shuffle
import copy

class SudokuGenerator:
	
	def __init__(self,grid=None):
		self.counter = 0
		
		#if a grid/puzzle is passed in, make a copy and solve it
		if grid:
			if len(grid[0]) == 9 and len(grid) == 9:
				self.grid = grid
				self.original = copy.deepcopy(grid)
				self.solve_input_sudoku()
			else:
				print("input needs to be a 9x9 matrix")
		else:
			#if no puzzle is passed, generate one
			self.grid = [[0 for i in range(9)] for j in range(9)]
			self.generate_puzzle()
			self.original = copy.deepcopy(self.grid)
		
		
	def solve_input_sudoku(self):
		self.generate_solution(self.grid)
		return

	def generate_puzzle(self):
		self.generate_solution(self.grid)
		self.print_grid('full solution')
		self.remove_numbers_from_grid()
		self.print_grid('\npuzzle with unique solution:')
		return

	def print_grid(self, grid_name=None):
		if grid_name:
			print(grid_name)
		for row in self.grid:
			print(row)
		return

	def num_used_in_row(self,grid,row,number):
		if number in grid[row]:
			return True
		return False

	def num_used_in_column(self,grid,col,number):
		for i in range(9):
			if grid[i][col] == number:
				return True
		return False

	def num_used_in_subgrid(self,grid,row,col,number):
		sub_row = (row // 3) * 3
		sub_col = (col // 3)  * 3
		for i in range(sub_row, (sub_row + 3)): 
			for j in range(sub_col, (sub_col + 3)): 
				if grid[i][j] == number: 
					return True
		return False

	def valid_location(self,grid,row,col,number):
		if self.num_used_in_row(grid, row,number):
			return False
		elif self.num_used_in_column(grid,col,number):
			return False
		elif self.num_used_in_subgrid(grid,row,col,number):
			return False
		return True

	def find_empty_square(self,grid):
		for i in range(9):
			for j in range(9):
				if grid[i][j] == 0:
					return (i,j)
		return

	def solve_puzzle(self, grid):
		for i in range(0,81):
			row=i//9
			col=i%9
			if grid[row][col]==0:
				for number in range(1,10):
					if self.valid_location(grid,row,col,number):
						grid[row][col]=number
						if not self.find_empty_square(grid):
							self.counter+=1
							break
						else:
							if self.solve_puzzle(grid):
								return True
				break
		grid[row][col]=0  
		return False

	def generate_solution(self, grid):
		number_list = [1,2,3,4,5,6,7,8,9]
		for i in range(0,81):
			row=i//9
			col=i%9
			if grid[row][col]==0:
				shuffle(number_list)      
				for number in number_list:
					if self.valid_location(grid,row,col,number):
						grid[row][col]=number
						if not self.find_empty_square(grid):
							return True
						else:
							if self.generate_solution(grid):
								return True
				break
		grid[row][col]=0  
		return False

	def get_non_empty_squares(self,grid):
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0:
					non_empty_squares.append((i,j))
		shuffle(non_empty_squares)
		return non_empty_squares

	def remove_numbers_from_grid(self):
		non_empty_squares = self.get_non_empty_squares(self.grid)
		non_empty_squares_count = len(non_empty_squares)
		rounds = 3
		while rounds > 0 and non_empty_squares_count >= 17:
			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1
			removed_square = self.grid[row][col]
			self.grid[row][col]=0
			grid_copy = copy.deepcopy(self.grid)
			self.counter=0      
			self.solve_puzzle(grid_copy)
			if self.counter!=1:
				self.grid[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1
		return

new_puzzle = SudokuGenerator()


import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

N = 10
ON = 255
OFF = 0
vals = [ON, OFF]

# populate grid with random on/off - more off than on
# grid = np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)
grid = np.zeros((N, N))
grid[1, 5] = ON
grid[1, 6] = ON
grid[1, 4] = ON

def update(data):
	global grid
	# copy grid since we require 8 neighbors for calculation
	# and we go line by line 
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N):
			# compute 8-neghbor sum 
			# using toroidal boundary conditions - x and y wrap around 
			# so that the simulaton takes place on a toroidal surface.
			total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
					 grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
					 grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
					 grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) / 255
			# apply Conway's rules
			if grid[i, j] == ON:
				if total < 2 or total > 3:
					newGrid[i, j] = OFF
			else:
				if total == 3:
					newGrid[i, j] = ON
  # update data
	mat.set_data(newGrid)
	grid = newGrid
	return [mat]

# set up animation
fig, ax = plt.subplots()

for i in range(1, N+1):
	ax.text(-0.1, i, f'{i}', va='center', ha='center')
	ax.text(i, -0.1, f'{i}', va='center', ha='center')

mat = ax.matshow(grid, cmap='Greys')
plt.xticks(np.arange(0.5, N+0.5, 1), [])
plt.yticks(np.arange(0.5, N+0.5, 1), [])
plt.xlim(0.5, N+0.5)
plt.ylim(0.5, N+0.5)
plt.grid()

if N <= 40:
	scale = 5
elif N >= 40 and N <= 80:
	scale = 20
else:
	scale = 30
fig.set_figheight(scale)
fig.set_figwidth(scale)

ani = animation.FuncAnimation(fig, update, interval=500, save_count=100)

ani.save('gif.gif')

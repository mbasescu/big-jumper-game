Note: This game is mostly a learning exercise and is a work in progress so it might not work well, or might not work the way you think it should.

Dependencies:
- python3
- pygame

To run the program, type:
"python3 BigJumperGame.py"

The current behavior is simply a mass/spring/damper simulation with vertical gravity, using a velocity Verlet integrator. The spring is linear and in-line with the mass, although I made the visualized linkages to give the illusion that it is a torsional spring instead.

Fun changes/improvements include:
- Add better support for different size upper and lower body linkages
	This is already almost supported, I just need to solve the system of equations in the comments which would calculate the required linkage angles

- Add controllability of the character

- "Double bounce" style super-jumps or anti-jumps (hit spacebar at correct timing to amplify or negate spring energy)

- Spring compression limit with proper dynamics handling to prevent going through the floor

- Variable height floor handling for platforming

- Camera following for platforming

- "Boingier" spring (has visual oscillations after releasing from jump)

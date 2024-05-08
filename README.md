This repo will store each optimization strategy I've made

Optimization strategies, as I understand them, are algorithms that attempt finding the solution to a given problem with the use of multiple agents. A famous problem that proves
the worth of these strategies is the traveling salesman problem in which the goal is to travel to each given point once while ensuring each of these points were met.

The listed strategies include:
  1) Particle Swarm Optimization (pso)

1)
Particle Swarm Optimization is a stochastic meta-heuristic optimization strategy used to find the best solution for a given task within a set time by using multiple agents dubbed
as particles. Each particle spawns with a random position and velocity where velocity is updated by adding the inertia, cognitive, and social components together and the position
is updated by adding the position of old and new velocity together.

The inertia component is the product of the inertia weight and current velocity.
The cognitive component is the product of a random # between 0-1, the exploration coefficient, and the difference between the particle's best position and its current position.
The social component is the product of a random # between 0-1, the exploitation coefficient and the difference between the best position found overall and its current position.

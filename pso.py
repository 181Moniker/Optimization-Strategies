#particle swarm optimization
import pygame, sys
import random as r
import math as m
import time as t
import matplotlib.pyplot as plt
#1317 652
#iter_num = int(input("How many iterations do you want? "))
class Particle():
    def __init__(self, width, height, width_dev, height_dev, target, iters):
        self.x_dev = width_dev
        self.y_dev = height_dev

        self.width = width
        self.height = height

        self.position = [r.randint(0, width), r.randint(0,height)]
        self.velocity = [r.uniform(-1,1), r.uniform(-1,1)]

        self.global_best_pos = target
        self.best_pos = self.position.copy()
        self.direction = 'r'
        self.comparative_coords = (0,0)
        self.target = target
        self.distance_from_global = None
        self.hit_mark = False

        self.w = 0.9
        self.c1 = 2
        self.c2 = 2
        self.iters_str_len = len(str(iters))

        place = "10"
        minuend="0.0"
        zeros=len(str(iters)) - 1

        for i in range(zeros): place+="0"; minuend+="0"
        place = int(place)

        change_to_one_at = len(minuend)-2
        minuend=[*minuend]; minuend[change_to_one_at]=1
        min = ""
        for i in range(len(minuend)): min+=str(minuend[i])
        minuend=float(min)

        self.subtrahend = self.restrict((minuend-(9/place)), self.iters_str_len)
        
    def restrict(self, x, length): return float(f"%.{length}f" %x)

    def set_gbpos(self, gbpos): self.global_best_pos = gbpos

    def set_direction(self, dir): self.direction = dir

    def get_cpos(self): return (self.position[0], self.position[1])

    def compare_with_personal_best(self):
        if m.fabs(self.position[0]-self.global_best_pos[0]) < m.fabs(self.best_pos[0]-self.global_best_pos[0]): self.best_pos = [self.position[0], self.best_pos[1]]
        if m.fabs(self.position[1]-self.global_best_pos[1]) < m.fabs(self.best_pos[1]-self.global_best_pos[1]): self.best_pos = [self.best_pos[0], self.position[1]]

    def update_velocity(self):
        '''
        This first part updates the velocity
        '''
        #vi(t+1) = wvi(t) + c1*r1*(pi-xi(t)) + c2*r2*(p_global - xi(t))
        #vi(t) is the currently velocity : xi(t) is the current position
        #pi is the particle's best position : p_global is the world's best positions
        #w is the inertia weight the controls the impact of the previous velocity
        c1, c2 = 2, 2; r1, r2 = r.random(), r.random()
        
        inertia_weight = [self.velocity[0]*self.w, self.velocity[1]*self.w]
        self.w -= self.subtrahend; self.w=self.restrict(self.w, self.iters_str_len)
        self.c1 -= self.subtrahend; self.c1=self.restrict(self.c1, self.iters_str_len)
        self.c2 -= self.subtrahend; self.c2=self.restrict(self.c2, self.iters_str_len)

        cognitive_comp = [(self.best_pos[0]-self.position[0])*c1*r1, (self.best_pos[1]-self.position[1])*c2*r2]
        social_comp = [(self.global_best_pos[0]-self.position[0])*c1*r1, (self.global_best_pos[1]-self.position[1])*c2*r2]

        new_velocity = [(inertia_weight[0]+cognitive_comp[0]+social_comp[0]), (inertia_weight[1]+cognitive_comp[1]+social_comp[1])]
        self.velocity=new_velocity

    def update_position(self,show=False):
        new_position = [(self.position[0]+self.velocity[0]), (self.position[1]+self.velocity[1])]
        self.position = new_position
        if show == True: print("NEW POS:", self.position)
        self.maintain_bounds()
        self.compare_with_personal_best()

    def find_dist_from_global(self):
        self.distance_from_global = m.sqrt(pow((self.global_best_pos[0] - self.position[0]),2) + pow((self.global_best_pos[1] - self.position[1]), 2))
        return self.distance_from_global
    
    def get_global_pos(self, x):
        if x == self.distance_from_global: return self.position
        else: return None

    def position_to_global(self):
        #if self.hit_mark == True: return True
        #else:
        #if self.position == self.global_best_pos: self.hit_mark = True; return True
        leeway = 7
        if ((self.position[0]-leeway) <= self.global_best_pos[0] <= (self.position[0]+leeway)) and ((self.position[1]-leeway) <= self.global_best_pos[1] <= (self.position[1]+leeway)): self.hit_mark = True; return True
        else: return False

    def maintain_bounds(self):
        self.position[0] = max(self.x_dev, min(self.width-self.x_dev, self.position[0]))
        self.position[1] = max(self.y_dev, min(self.height-self.y_dev, self.position[1]))

def pso(screen, width, height, clock, font_one, reps=0, ptcles=[], targ=(0,0)):
    iterations = 0
    best_global_pos = (0,0)
    start = t.perf_counter()
    baseline = 0
    record_accur = {}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill("white")
        #Stats on left side of screen
        iter_tracker = font_one.render(f'Iterations: {iterations}/{reps}', False, (24,24,24))
        iter_tracker_rect = iter_tracker.get_rect(center = (width - 158, 28))
        screen.blit(iter_tracker, iter_tracker_rect);

        particle_num = font_one.render(f'Particles: {len(ptcles)}', False, (24,24,24))
        particle_num_rect = particle_num.get_rect(center=(width - 132.3, 58))
        screen.blit(particle_num, particle_num_rect);

        #Stats on right side of screen
        screen_dim = font_one.render(f'Height: {height} | Width: {width}', False, (24,24,24))
        screen_dim_rect = screen_dim.get_rect(center=(193, 58))
        screen.blit(screen_dim, screen_dim_rect);

        pygame.draw.circle(screen, "red", targ, 12)
        target_at = font_one.render(f'Target Position: {targ} | Best Global Position: {(float("%.2f" %best_global_pos[0]) , float("%.2f" %best_global_pos[1]))}', False, (24,24,24))
        target_at_rect = target_at.get_rect(center=(472.5, 28))
        screen.blit(target_at, target_at_rect);

        for i in range(len(ptcles)): 
            pygame.draw.circle(screen, "black",ptcles[i].get_cpos(), 10)

        pygame.display.update(); clock.tick(60) #;dt = clock.tick(60)/1000

        comparative_pos = []

        for i in range(len(ptcles)):
            comparative_pos.append(ptcles[i].find_dist_from_global())
            if comparative_pos[i] == None:
                print("stuck")
                while True: pass
            ptcles[i].update_velocity()
            ptcles[i].update_position()

        comparative_pos.sort()
        for i in range(len(ptcles)):
            if ptcles[i].get_global_pos(comparative_pos[0]) != None:
                best_global_pos = ptcles[i].get_global_pos(comparative_pos[0])

        #if iterations == 1 or (iterations==(reps*0.25)) or (iterations==(reps*0.50)) or (iterations==(reps*0.75)): t.sleep(10)
        if iterations == reps: return record_accur
        iterations+=1;
    
        time = float("%.2f" %(t.perf_counter() - start))
        #print("The time:", time)
        sec = str(time-baseline)
        #match (time-baseline):
        if "1.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "2.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "3.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "4.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "5.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "6.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "7.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "8.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "9.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]
        if "10.0" in sec: record_accur[time]=[ptcles[i].position_to_global() for i in range(len(ptcles))]

def graph_coords(dct):
    x_axis, y_axis = [], []
    num_of_trues = 0
    for key in dct: x_axis.append(key); y_axis.append(dct[key])

    for i in range(len(y_axis)):
        for j in range(len(y_axis[i])):
            if y_axis[i][j] == True: num_of_trues+=1
        y_axis[i] = num_of_trues; num_of_trues = 0

    #x_removal, y_removal = [], []
    #for i in range(len(x_axis)): if ".01" or ".0" not in str(x_axis[i])
    print("keys:", x_axis); print("vals:", y_axis)

    plt.bar(x_axis, y_axis, 0.4)
    plt.xlabel("Seconds")
    plt.ylabel("Particle Success in Meeting Mark")
    plt.title("Marks per Second")
    plt.show()

def start_program():
    height = 660; width = 1320 #dimensions for window
    y_dev = 92; x_dev = 0 #bounds for window
    adj_width = width-100; adj_height = height-100
    target_pos = [r.randrange(0, adj_width), r.randrange(0, adj_height)]
    target_pos[0] = max(x_dev, min(width-x_dev, target_pos[0]))
    target_pos[1] = max(y_dev, min(height-y_dev, target_pos[1]))
    target_pos = (target_pos[0], target_pos[1])
    reps = int(input("How many repetitions do you want? "))

    while True:
        try:
            particles = [Particle(width, height, x_dev, y_dev, target_pos, reps) for _ in range(int(input("How many particles do you want? ")))]
            #pygame init
            pygame.init()
            screen = pygame.display.set_mode((width, height))

            clock = pygame.time.Clock()
            font_one = pygame.font.Font('C:/Users/Jonathan/Documents/Work/Research/Swarm Protocols/Particle Swarm Optimization/Swarm Progress/Pixeltype.ttf', 50)

            #start = t.perf_counter()            
            graph_coords(pso(screen, width, height, clock, font_one, reps, particles, target_pos))
            #finish = t.perf_counter()
            break
        except ValueError: print("***PLEASE ENTER AN INTEGER***"); t.sleep(3)

    choice = input("Rerun program? Yes(1) | No(any key): ")
    if choice == "1": start_program()
    else: print("***EXITING PROGRAM***")

start_program()




'''
Consider path of particles to point: 
    map out surrounding area?
'''
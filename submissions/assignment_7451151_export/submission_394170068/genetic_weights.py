import numpy as np
import random
from breakthrough import play_game
from breakthrough_agent import AlphaBetaAgent
from breakthrough import phi
from tqdm import tqdm
POP_SIZE = 100
GENERATIONS = 100
SEARCH_DEPTH = 2
MUTATION_RATE = 0.3
MUTATION_STD = 1.0
ELITE_PERCENT = 0.2
MATCH_PERCENT = 0.1


def create_individual():
    return np.random.uniform(-3, 3, 8)


def build_eval_fn(weights):
    def eval_fn(state, player):
        features = phi(state, player)
        return features @ weights.T
    return eval_fn


INITIAL_ELO = 1000
K_FACTOR = 32

def expected_score(rA, rB):
    return 1 / (1 + 10 ** ((rB - rA) / 400))

def update_elo(rA, rB, scoreA):
    expA = expected_score(rA, rB)
    newA = rA + K_FACTOR * (scoreA - expA)
    newB = rB + K_FACTOR * ((1 - scoreA) - (1 - expA))
    return newA, newB

def evaluate_population(population):
    n = len(population)

    ratings = np.ones(n) * INITIAL_ELO

    num_matches = max(1, int(n * MATCH_PERCENT))

    eval_fns = [build_eval_fn(w) for w in population]

    
    matches = []
    for i in range(n):
        opponents = random.sample(
            [j for j in range(i + 1, n)],
            min(num_matches, n - i - 1)
        )
        for j in opponents:
            matches.append((i, j))

    random.shuffle(matches)

    for i, j in tqdm(matches):

        white = AlphaBetaAgent("A", depth=SEARCH_DEPTH, eval_fn=eval_fns[i])
        black = AlphaBetaAgent("B", depth=SEARCH_DEPTH, eval_fn=eval_fns[j])

        result = play_game(
            white,
            black,
            max_moves=80,
            display=False,
            progress=False
        )

        if result["winner"] == "white":
            score_i = 1
        elif result["winner"] == "black":
            score_i = 0
        else:
            score_i = 0.5

        ratings[i], ratings[j] = update_elo(
            ratings[i], ratings[j], score_i
        )

    return ratings



def select_parents(population, fitness):
    idx = np.random.choice(len(population), size=3, replace=False)
    best = idx[np.argmax(fitness[idx])]
    return population[best]




def crossover(parent1, parent2):
    mask = np.random.rand(len(parent1)) > 0.5
    child = np.where(mask, parent1, parent2)
    return child




# def mutate(individual):
#     if random.random() < MUTATION_RATE:
#         individual += np.random.normal(0, MUTATION_STD, size=len(individual))
#     return individual

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] += np.random.normal(0, MUTATION_STD)
    return individual


def evolve():
    population = [create_individual() for _ in range(POP_SIZE)]
    population.append(np.array([2,0,0,0,0,0,0,0]))
    population.append(np.array([0,-2,0,0,0,0,0,64]))
    population.append(np.array([-2.84715749, -2.0439127,   1.94531968, -1.30766562,  1.17206287, -2.79700373, -0.13782156,  1.47244376]))
    population.append(np.array([-5.82664428,  1.06427708, -0.90816662, -1.30766562,  1.37431272, -2.95610787, -0.55881905,  0.75327318]))
    
    for gen in range(GENERATIONS):
        print(f"\nGeneration {gen}")


        ratings = evaluate_population(population)
        fitness = ratings
        ranked = np.argsort(fitness)[::-1]

        print("Best fitness:", fitness[ranked[0]])
        print("Best weights:", population[ranked[0]])

        # Elitism
        survivors = [population[i] for i in ranked[:int(POP_SIZE * ELITE_PERCENT)]]

        # Reproduce
        new_population = survivors.copy()
        new_population.append(np.array([2,0,0,0,0,0,0,0]))
        new_population.append(np.array([0,-2,0,0,0,0,0,64]))
        
        
        while len(new_population) < POP_SIZE:
            p1 = select_parents(population, fitness)
            p2 = select_parents(population, fitness)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    # Final best
    fitness = evaluate_population(population)
    best_idx = np.argmax(fitness)
    print("\nFinal Best Weights:")
    print(population[best_idx])

    return population[best_idx]


if __name__ == "__main__":
    best_weights = evolve()
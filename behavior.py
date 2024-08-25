import random
from environment import Env

class Animal:
    def __init__(self, env, current_zone=None, exploration_rate=0.9):
        self.env = env
        self.current_zone = current_zone
        self.memory = {}
        self.exploration_rate = exploration_rate
        self.iteration = 0  # Dodajemy licznik iteracji
        self.last_chosen_zone = None
        self.zone_efficiency_rate = {'A1': {'success': 0, 'failure': 0, 'last_visited': 0},
                                     'A2': {'success': 0, 'failure': 0, 'last_visited': 0},
                                     'A3': {'success': 0, 'failure': 0, 'last_visited': 0},
                                     'B1': {'success': 0, 'failure': 0, 'last_visited': 0},
                                     'B2': {'success': 0, 'failure': 0, 'last_visited': 0},
                                     'B3': {'success': 0, 'failure': 0, 'last_visited': 0}}
        self.threshold = 10
        
    def move(self):
        if random.random() < self.exploration_rate:
            # Eksploracja
            chosen_zone = random.choice(self.env.get_zones())
            print("Exploring new zone...")
        else:
            # Eksploatacja pamięci
            if self.memory:
                best_zone_id = max(self.memory, key=self.memory.get)
                chosen_zone = next(zone for zone in self.env.get_zones() if zone['id'] == best_zone_id)
                print(f"Exploiting known good zone: {best_zone_id}")
            else:
                chosen_zone = random.choice(self.env.get_zones())
        
        self.current_zone = chosen_zone['id']
        self.last_chosen_zone = chosen_zone
        self.zone_efficiency_rate[self.current_zone]['last_visited'] = self.iteration
        print(f"Animal moved to {self.current_zone}.")
        
        if chosen_zone["food"] > 0:
            print(f"Animal found food at {self.current_zone}!")
            self.zone_efficiency_rate[self.current_zone]['success'] += 1
        else:
            print(f"Animal didn't find food at {self.current_zone}.")
            self.zone_efficiency_rate[self.current_zone]['failure'] += 1
            
    def learn(self):
        self.update_efficiency_rate()

        if self.zone_efficiency_rate[self.current_zone]['efficiency'] < self.threshold:
            print(f"Efficiency of {self.current_zone} zone is below threshold. Considering avoiding this zone.")
        else:
            if self.last_chosen_zone["food"] > 0:
                self.exploration_rate = max(0.1, self.exploration_rate * 0.99)
                print(f"Exploration rate updated to {self.exploration_rate:.3f}")
            else:
                # Możesz tutaj dodać inny mechanizm, np. wolniejsze zwiększanie współczynnika eksploracji:
                self.exploration_rate = min(1, self.exploration_rate * 1.005)
                print(f"Exploration rate increased slowly to {self.exploration_rate:.3f}")
        
        self.decay_memory()


        
    def decay_memory(self):
        for zone, data in self.zone_efficiency_rate.items():
            time_since_last_visit = self.iteration - data['last_visited']
            if time_since_last_visit > 5:  # Przykładowy próg zapominania
                data['success'] *= 0.9  # Zmniejszanie sukcesów
                data['failure'] *= 0.9  # Zmniejszanie porażek
                print(f"Memory of zone {zone} decayed due to inactivity.")

    def update_efficiency_rate(self):
        success = self.zone_efficiency_rate[self.current_zone]['success']
        failure = max(1, self.zone_efficiency_rate[self.current_zone]['failure'])
        
        success_rate = success / (success + failure)
        self.zone_efficiency_rate[self.current_zone]['efficiency'] = success_rate * 100
            
if __name__ == "__main__":
    env = Env()
    animal = Animal(env)
    
    while True:
        env.generate_food()
        animal.move()
        animal.learn()
        
        # Wyświetlanie współczynnika eksploracji w każdej iteracji
        print(f"Iteration {animal.iteration}: Exploration rate = {animal.exploration_rate:.3f}")
        
        animal.iteration += 1  # Zwiększamy licznik iteracji

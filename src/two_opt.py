from src.route import Route
from src.utils import timer

class TwoOpt:
    ''' Class for the 2-opt heuristic '''
    
    def __init__(self, routes: list[Route]):
        self.routes = routes
    
    @timer
    def run(self) -> tuple[float, list[Route]]:
        ''' Run the 2-opt heuristic '''
        
        routes: list[Route] = []
        
        for idx in range(len(self.routes)):
            route = self.routes[idx]
            
            while True:
                best = route.best_reversed()
                    
                if best.cost < route.cost:
                    route = best
                else:
                    break
            
            routes.append(route)   
            
        return routes
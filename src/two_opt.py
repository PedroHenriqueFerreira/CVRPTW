from src.route import Route
from src.utils import timer

class TwoOpt:
    ''' Class for the 2-opt heuristic '''
    
    @timer
    def run(self, routes: list[Route]) -> tuple[float, list[Route]]:
        ''' Run the 2-opt heuristic '''
        
        for idx, route in enumerate(routes):
            best_route = route
            
            while True:
                improved = False
                
                for i in range(len(route) - 1):
                    for j in range(i + 1, len(route)):
                        new_route = route.reversed(i, j + 1)
                        
                        if new_route.cost < best_route.cost and new_route.time != float('inf'):
                            best_route = new_route
                            improved = True        
                
                route = best_route
                
                if not improved:
                    break
            
            routes[idx] = route
            
        return routes
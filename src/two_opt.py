from src.route import Route
from src.utils import timer

class TwoOpt:
    ''' Class for the 2-opt heuristic '''
    
    @timer
    def run(self, routes: list[Route]) -> tuple[float, list[Route]]:
        ''' Run the 2-opt heuristic '''
        
        out: list[Route] = []
        
        for idx in range(len(routes)):
            route = best_route = routes[idx]
            
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
            
            out.append(route)   
            
        return out
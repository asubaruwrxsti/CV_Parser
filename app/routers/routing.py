from fastapi import APIRouter, Depends
from app.services import service
import pkgutil
import importlib

router = APIRouter(dependencies=[Depends(service.CORS)])

@router.get("/routes")
def get_routes():
    routes = []

    prohibited_routes = [
        '/auth',
        '/routing',
        '/users'
    ]

    # get all routers in the app.routers package
    package_name = 'app.routers'
    package = importlib.import_module(package_name)

    # Iterate through the modules in the package
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f'{package_name}.{module_name}')

        # Check if the module has a 'router' attribute
        if hasattr(module, 'router') and f'/{module_name}' not in prohibited_routes:
            # Include the router in the FastAPI app with a prefix
            routes.append(f'{module_name}')
    
    return {"routes": routes}

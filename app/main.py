from fastapi import FastAPI, Depends, Request
import pkgutil
import importlib
from app.dependencies import DatabaseSingleton

app = FastAPI()

package_name = 'app.routers'
package = importlib.import_module(package_name)

# Iterate through the modules in the package
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f'{package_name}.{module_name}')

    # Check if the module has a 'router' attribute
    if hasattr(module, 'router'):
        # Include the router in the FastAPI app
        app.include_router(module.router)

@app.get("/")
async def read_root(request: Request, db: DatabaseSingleton = Depends(DatabaseSingleton.get_instance)):
    with db.connection.cursor() as cursor:
        cursor.execute("INSERT INTO visits (user_agent, ip) VALUES (%s, %s)", (request.headers['user-agent'], request.client.host))
        cursor.execute("SELECT COUNT(*) FROM visits;")
        visits = cursor.fetchone()[0]
        db.commit()

    return {"Hello": "World", "Visits": visits}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

from fastapi import FastAPI, Depends, Request
import pkgutil
import importlib
from app.dependencies import get_database

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

# Define main routes
@app.get("/")
async def read_root(request: Request, db = Depends(get_database)):
    db.query("CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, user_agent VARCHAR(255), ip VARCHAR(255), visited_at TIMESTAMP DEFAULT NOW()); SELECT COUNT(*) FROM visits;")[0][0]
    db.query("INSERT INTO visits (user_agent, ip) VALUES (%s, %s)", (request.headers['user-agent'], request.client.host))
    visits = db.query("SELECT COUNT(*) FROM visits;")[0][0]

    return {"Hello": "World", "Visits": visits}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

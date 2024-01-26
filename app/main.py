from fastapi import FastAPI, Depends, Request
import pkgutil
import importlib
from app.dependencies import get_db, Database
from app.models import Visit

app = FastAPI()

package_name = 'app.routers'
package = importlib.import_module(package_name)

# Iterate through the modules in the package
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f'{package_name}.{module_name}')

    # Check if the module has a 'router' attribute
    if hasattr(module, 'router'):
        # Include the router in the FastAPI app with a prefix
        app.include_router(module.router, prefix=f'/{module_name}')

@app.get("/")
async def read_root(request: Request, db: Database = Depends(get_db)):
    visit = Visit(user_agent=request.headers['user-agent'], ip=request.client.host)
    await visit.create_record(db)

    visit_count = await visit.get_records(db)
    return {"Hello": "World", "visit_count": len(visit_count) if visit_count else 0}


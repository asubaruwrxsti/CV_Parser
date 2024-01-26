from fastapi import FastAPI, Depends, Request
import pkgutil
import importlib
from app.dependencies import get_db, Database

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
async def read_root(request: Request, db: Database = Depends(get_db)):
    try:
        db.query(
            "INSERT INTO visits (user_agent, ip) VALUES (%s, %s)",
            (request.headers['user-agent'], request.client.host)
        )
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        visit_count = db.query("SELECT COUNT(*) FROM visits")[0][0]

    return {"Hello": "World", "visit_count": visit_count}


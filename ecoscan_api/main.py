from fastapi import FastAPI

# router
from report_analysis_and_storage import report_analysis
from ecoagent import eco_agent


app = FastAPI()

# including routers
app.include_router(report_analysis.router)
app.include_router(eco_agent.router)
# app.include_router(user.router)
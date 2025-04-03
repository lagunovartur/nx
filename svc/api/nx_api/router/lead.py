from nx_api.svc.crud.router import crud_router, add_list_route
from nx_api.svc.lead.svc import LeadSvc, LeadList

router = crud_router(LeadSvc)
add_list_route(router, LeadList)

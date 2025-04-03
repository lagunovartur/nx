from dishka import Provider, Scope, provide

from nx_api.svc.lead.svc import LeadSvc, LeadList


class LeadProv(Provider):
    crud_svc = provide(LeadSvc, scope=Scope.REQUEST)
    list_svc = provide(LeadList, scope=Scope.REQUEST)

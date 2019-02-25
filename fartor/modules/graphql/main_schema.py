import graphene

from fartor.apps.accounting.users.actions.login import LoginMutation
from fartor.apps.accounting.users.actions.self import GetSelfQuery


class Queries(GetSelfQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(graphene.ObjectType):
    login = LoginMutation.Field()


schema = graphene.Schema(query=Queries, mutation=Mutations)

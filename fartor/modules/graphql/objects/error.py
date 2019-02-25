import graphene


class GraphqlError(graphene.ObjectType):
    code = graphene.String(description="Error identifier")
    description = graphene.String(description="Error description")
    status = graphene.Int(description="Error status code")

    class Meta:
        description = "This object represent an error"

    @staticmethod
    def resolve_code(error, *args, **kwargs):
        return error.get('code', 'unknown_error')

    @staticmethod
    def resolve_description(error, *args, **kwargs):
        return error.get('description', None)

    @staticmethod
    def resolve_status(error, *args, **kwargs):
        return error.get('status', 500)

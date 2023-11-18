from graphql_auth.schema import MeQuery, UserQuery
import graphene
from graphql_auth import mutations
from graphqlAPI.nodes import UsersNode
from graphql_jwt.decorators import login_required
from graphqlAPI.mutation import CreateUserWithProfileMutation, UpdateUserWithProfileMutation, CreatePostMutation, PostLikeMutation
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField



class Mutation(MeQuery,UserQuery,graphene.ObjectType):
    signUp = CreateUserWithProfileMutation.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_user = UpdateUserWithProfileMutation.Field()
    create_post = CreatePostMutation.Field()
    post_like = PostLikeMutation.Field()


class fQuery(graphene.ObjectType):
    users = graphene.List(UsersNode)
    user_by_id = graphene.Field(UsersNode, id=graphene.Int(required=True))

    @login_required
    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)

    @login_required
    def resolve_users(self,info):
        print("=-=-auth-==-=-=")
        return User.objects.all()


class Query(MeQuery,UserQuery,fQuery,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)


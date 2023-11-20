from graphql_auth.schema import MeQuery, UserQuery
import graphene
from graphql_auth import mutations
from graphqlAPI.nodes import UsersNode, PostNode
from graphql_jwt.decorators import login_required, refresh_token_lazy
from graphqlAPI.mutation import CreateUserWithProfileMutation, UpdateUserWithProfileMutation, CreatePostMutation, PostLikeMutation
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField
from restAPI.models import Post
from graphqlAPI.filters import PostFilterSet, UserFilter


class Mutation(MeQuery,UserQuery,graphene.ObjectType):
    signUp = CreateUserWithProfileMutation.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_user = UpdateUserWithProfileMutation.Field()
    create_post = CreatePostMutation.Field()
    post_like = PostLikeMutation.Field()


class fQuery(graphene.ObjectType):
    users = DjangoFilterConnectionField(UsersNode)
    user_by_id = graphene.Field(UsersNode, id=graphene.Int(required=True))
    all_posts = DjangoFilterConnectionField(PostNode,filterset_class=PostFilterSet)

    @login_required
    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)

    @login_required
    def resolve_users(self,info,**kwargs):
        return User.objects.all()

    @login_required
    def resolve_all_posts(self, info, **kwargs):
        print(11111111111111)
        return Post.objects.all()

class Query(MeQuery,UserQuery,fQuery,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)


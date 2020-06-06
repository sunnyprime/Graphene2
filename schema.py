import graphene
import json
import uuid
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime()

class Query(graphene.ObjectType):
    users = graphene.List(User,limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info,limit=None):
        return True
    
    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Fred",created_at=datetime.now()),
            User(id="2", username="Dough",created_at=datetime.now())
        ][:limit]

class createUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self,info,username):
        user = User(id="3", username=username,
        created_at=datetime.now())
        return createUser(user=user)

class Mutation(graphene.ObjectType):
    user = User(username=username)
    create_user = createUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    mutation {
        createUser(username: "Jeff") {
            user {
                id
                username
                createdAt
            }
        }
    }
    '''
)

# print(result.data.items())
# print(result.data['hello'])

dictResult = dict(result.data.items())
# print(json.dumps(dictResult))
print(json.dumps(dictResult,indent=2))
# print(type(result.data))



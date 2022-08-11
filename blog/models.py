import datetime

from redis_om import get_redis_connection, EmbeddedJsonModel, JsonModel, Field, Migrator

redis = get_redis_connection(
    host="redis-14531.c13.us-east-1-3.ec2.cloud.redislabs.com",
    port=14531,
    password="TbuxEUkupHczh3G5SVYFr2tF1SPmILDk",
    decode_responses=True,
)


class Author(EmbeddedJsonModel):
    first_name: str = Field(index=True, full_text_search=True)
    last_name: str
    email: str
    bio: str
    date_joined: datetime.date = Field(default=datetime.datetime.now())

    class Meta:
        database = redis


class Blog(JsonModel):
    title: str = Field(index=True, full_text_search=True)
    content: str
    author: Author
    date_posted: datetime.date = Field(
        default=datetime.datetime.today().strftime("%Y-%m-%d")
    )

    class Meta:
        database = redis


Migrator().run()

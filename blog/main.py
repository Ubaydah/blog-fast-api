from fastapi import FastAPI
from models import Author, Blog

from redis_om.model import NotFoundError

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}


# create an author
@app.post("/authors")
async def create_author(body: Author):
    author = Author(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        bio=body.bio,
        date_joined=body.date_joined,
    )

    author.save()

    return author


# create a blog
@app.post("/blogs")
async def create_blog(body: dict):
    author = Author.get(body["author_id"])
    blog = Blog(title=body["title"], content=body["content"], author=author)

    blog.save()

    return blog


# get a blog
@app.get("/blogs/{pk}")
async def get_blog(pk: str):
    try:
        blog = Blog.get(pk)
    except NotFoundError:
        return {"error": "no resource found"}
    return blog


# update a blog
@app.put("/blogs/{pk}")
async def update_blog(pk: str, body: dict):
    blog = Blog.get(pk)

    blog.title = body["title"]
    blog.content = body["content"]

    blog.save()

    return blog


# delete a blog
@app.delete("/blogs/{pk}")
async def delete_blog(pk: str):
    Blog.delete(pk)
    return {"success": "blog deleted successfully"}


def format_results(data):
    response = []
    for dat in data:
        response.append(dat.dict())

    return {"results": response}


@app.post("/blogs/find")
async def blog_by_name(title: str):
    blogs = Blog.find(Blog.title % title).all()

    return format_results(blogs)


@app.post("/blogs/find/author")
async def blog_by_author(first_name: str):
    blogs = Blog.find(Blog.author.first_name == first_name).all()

    return format_results(blogs)

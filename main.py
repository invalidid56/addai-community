from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoint.user.route import router as user_router
from endpoint.article.route import router as article_router
from endpoint.comment.route import router as comment_router


tags_metadata = [
    {
        "name": "User",
        "description": "유저와 관련된 API 엔드포인트를 정의합니다.",
    },
    {
        "name": "Article",
        "description": "불판과 관련된 API 엔드포인트를 정의합니다.",
    },
    {
        "name": "Comment",
        "description": "장작과 관련된 API 엔드포인트를 정의합니다.",
    }
]


app = FastAPI(
    title="AddAI-Community API",
    summary="AddAI-Community 서비스의 API 서버입니다.",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(article_router)
app.include_router(comment_router)


@app.on_event("startup")
async def startup():
    print("APP STARTUP")


@app.on_event("shutdown")
async def shutdown():
    print("APP SHUTDOWN")



from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, index=True, nullable=False)

    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)

    banner_image = Column(String)   # S3 Link

    creator_id = Column(
        Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    creator = relationship("User", backref="articles")

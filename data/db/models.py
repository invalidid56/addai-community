from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Campaign(Base):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    budget_limit = Column(Integer, nullable=False)
    creator_id = Column(
        Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    creator = relationship("User", backref="campaigns")

    images = Column(String, nullable=False)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)

    content = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"))
    creator_id = Column(Integer, ForeignKey("user.id"))
    article = relationship("Article", backref="comments")


class Banner(Base):
    __tablename__ = "banner"

    id = Column(Integer, primary_key=True, index=True)
    image_link = Column(String)
    clicks = Column(Integer)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", backref="banners")


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, index=True, nullable=False)

    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)

    banner_id = Column(Integer, ForeignKey("banner.id"))

    creator_id = Column(
        Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    creator = relationship("User", backref="articles")

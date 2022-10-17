import datetime
from models.base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, UniqueConstraint, ForeignKeyConstraint, Index


class LikedPost(Base):
    __tablename__ = "liked_post"

    __table_args__ = (UniqueConstraint("users_id", "post_id", name="users_post_unique"),
                      ForeignKeyConstraint(["users_id"], ["users.id"])
                      )

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    users_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)


Index("liked_post_users_id_idx", LikedPost.users_id)

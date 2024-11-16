from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid




# 340 bytes
class User(Base):
    __tablename__ = "Users"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(60), nullable=True, unique=True)
    phone = Column(String(12), nullable=True)
    address = Column(String(200), nullable=True)
    password = Column(String(70), nullable=False, default="00000")

    # Relationship to Landlord model
    # landlord = relationship("Landlord", back_populates="user", uselist=False)

    def update(self, update_data: dict):
        # Helper method to update fields dynamically
        for key, value in update_data.items():
            setattr(self, key, value)


# class Landlord(Base):
#     __tablename__ = "Landlord"

#     lid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     uid = Column(UUID(as_uuid=True), ForeignKey('Users.uid'), nullable=False)

#     # Relationship back to User model
#     user = relationship("User", back_populates="landlord")
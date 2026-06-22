from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Websites(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(1024), nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    check_interval_seconds = Column(Integer, nullable=False, server_default=text("60"))
    timeout_in_seconds = Column(Integer, nullable=False, server_default=text("10"))
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("Users", back_populates="websites")
    website_checks = relationship("WebsiteChecks", back_populates="website", cascade="all, delete-orphan")
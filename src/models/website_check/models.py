from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

from src.core.database import Base

class WebsiteChecks(Base):
    __tablename__ = "website_checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    http_status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False)
    error_message = Column(String, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())

    website = relationship("Websites", back_populates="website_checks")
import enum

from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, Boolean, text, Enum
from sqlalchemy.orm import relationship

from src.core.database import Base


class ErrorType(enum.Enum):
    TIMEOUT = "timeout"
    DNS_ERROR = "dns_error"
    SSL_ERROR = "ssl_error"
    CONNECTION_ERROR = "connection_error"
    HTTP_ERROR = "http_error"
    OTHER_ERROR = "other_error"
    CONNECTION_TIMEOUT = "connection_timeout"
    READ_TIMEOUT = "read_timeout"
    WRITE_TIMEOUT = "write_timeout"
    POOL_TIMEOUT = "pool_timeout"
    INVALID_URL = "invalid_url"
    DECODING_ERROR = "decoding_error"
    PROTOCOL_ERROR = "protocol_error"


class WebsiteChecks(Base):
    __tablename__ = "website_checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    http_status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    is_available = Column(Boolean, nullable=False)

    error_type = Column(
        Enum(
            ErrorType,
            values_callable=lambda x: [e.value for e in x],
            name="error_type"
        ),
        nullable=True
    )
    error_message = Column(String, nullable=False)

    checked_at = Column(DateTime(timezone=True), server_default=func.now())

    website = relationship("Websites", back_populates="website_checks")

from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    our_url = Column(String, index=True)
    competitor_url = Column(String, index=True)
    our_score = Column(Integer)
    competitor_score = Column(Integer)
    report_data = Column(JSON)  # Stores the full JSON analysis result
    created_at = Column(DateTime, default=datetime.utcnow)

class GBPReport(Base):
    __tablename__ = "gbp_reports"

    id = Column(Integer, primary_key=True, index=True)
    profile_url = Column(String, index=True)
    business_name = Column(String)
    overall_score = Column(Integer)
    report_data = Column(JSON)  # Stores the full JSON GBP report
    created_at = Column(DateTime, default=datetime.utcnow)

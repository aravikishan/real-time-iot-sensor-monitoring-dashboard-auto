
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./iot_dashboard.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    status = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    threshold = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/sensors", response_class=HTMLResponse)
async def read_sensors(request: Request):
    return templates.TemplateResponse("sensors.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def read_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/alerts", response_class=HTMLResponse)
async def read_alerts(request: Request):
    return templates.TemplateResponse("alerts.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# API Endpoints
@app.get("/api/sensors")
async def get_sensors(db: Session = Depends(get_db)):
    sensors = db.query(Sensor).all()
    return sensors

@app.post("/api/sensors")
async def add_sensor(sensor: Sensor, db: Session = Depends(get_db)):
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor

@app.get("/api/data")
async def get_sensor_data(sensor_id: int, db: Session = Depends(get_db)):
    data = db.query(SensorData).filter(SensorData.sensor_id == sensor_id).all()
    return data

@app.post("/api/alerts")
async def create_alert(alert: Alert, db: Session = Depends(get_db)):
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@app.get("/api/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_active == True).all()
    return alerts

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

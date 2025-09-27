from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime, date
import os
from typing import Optional

# Tạo database
SQLALCHEMY_DATABASE_URL = "sqlite:///./transport.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    base_salary = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    routes = relationship("Route", back_populates="employee")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False)
    capacity = Column(Float)  # Trọng tải
    fuel_consumption = Column(Float)  # Tiêu hao nhiên liệu
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    routes = relationship("Route", back_populates="vehicle")

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_code = Column(String, nullable=False)  # NA_002, NA_004, etc.
    route_name = Column(String, nullable=False)
    distance = Column(Float)  # KM/Chuyến
    unit_price = Column(Float)  # Đơn giá
    employee_id = Column(Integer, ForeignKey("employees.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="routes")
    vehicle = relationship("Vehicle", back_populates="routes")
    daily_routes = relationship("DailyRoute", back_populates="route")

class DailyRoute(Base):
    __tablename__ = "daily_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    date = Column(Date, nullable=False)
    fuel_cost = Column(Float, default=0)
    fuel_quantity = Column(Float, default=0)
    fuel_price = Column(Float, default=0)
    trip_salary = Column(Float, default=0)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    route = relationship("Route", back_populates="daily_routes")

# Tạo bảng
Base.metadata.create_all(bind=engine)

# Dependency để lấy database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(title="Hệ thống quản lý vận chuyển")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Lấy thống kê tổng quan
    employees_count = db.query(Employee).count()
    vehicles_count = db.query(Vehicle).count()
    routes_count = db.query(Route).filter(Route.is_active == 1).count()
    today = date.today()
    daily_routes_count = db.query(DailyRoute).filter(DailyRoute.date == today).count()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "employees_count": employees_count,
        "vehicles_count": vehicles_count,
        "routes_count": routes_count,
        "daily_routes_count": daily_routes_count
    })

@app.get("/employees", response_class=HTMLResponse)
async def employees_page(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return templates.TemplateResponse("employees.html", {"request": request, "employees": employees})

@app.post("/employees/add")
async def add_employee(
    name: str = Form(...),
    phone: str = Form(""),
    base_salary: float = Form(0),
    db: Session = Depends(get_db)
):
    employee = Employee(name=name, phone=phone, base_salary=base_salary)
    db.add(employee)
    db.commit()
    return RedirectResponse(url="/employees", status_code=303)

@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return templates.TemplateResponse("vehicles.html", {"request": request, "vehicles": vehicles})

@app.post("/vehicles/add")
async def add_vehicle(
    license_plate: str = Form(...),
    capacity: float = Form(0),
    fuel_consumption: float = Form(0),
    db: Session = Depends(get_db)
):
    vehicle = Vehicle(license_plate=license_plate, capacity=capacity, fuel_consumption=fuel_consumption)
    db.add(vehicle)
    db.commit()
    return RedirectResponse(url="/vehicles", status_code=303)

@app.get("/routes", response_class=HTMLResponse)
async def routes_page(request: Request, db: Session = Depends(get_db)):
    routes = db.query(Route).filter(Route.is_active == 1).all()
    employees = db.query(Employee).all()
    vehicles = db.query(Vehicle).all()
    return templates.TemplateResponse("routes.html", {
        "request": request, 
        "routes": routes,
        "employees": employees,
        "vehicles": vehicles
    })

@app.post("/routes/add")
async def add_route(
    route_code: str = Form(...),
    route_name: str = Form(...),
    distance: float = Form(0),
    unit_price: float = Form(0),
    employee_id: int = Form(...),
    vehicle_id: int = Form(...),
    db: Session = Depends(get_db)
):
    route = Route(
        route_code=route_code,
        route_name=route_name,
        distance=distance,
        unit_price=unit_price,
        employee_id=employee_id,
        vehicle_id=vehicle_id
    )
    db.add(route)
    db.commit()
    return RedirectResponse(url="/routes", status_code=303)

@app.get("/daily", response_class=HTMLResponse)
async def daily_page(request: Request, db: Session = Depends(get_db)):
    routes = db.query(Route).filter(Route.is_active == 1).all()
    today = date.today()
    daily_routes = db.query(DailyRoute).filter(DailyRoute.date == today).all()
    return templates.TemplateResponse("daily.html", {
        "request": request,
        "routes": routes,
        "daily_routes": daily_routes,
        "today": today
    })

@app.post("/daily/add")
async def add_daily_route(
    route_id: int = Form(...),
    date: str = Form(...),
    fuel_cost: float = Form(0),
    fuel_quantity: float = Form(0),
    fuel_price: float = Form(0),
    trip_salary: float = Form(0),
    notes: str = Form(""),
    db: Session = Depends(get_db)
):
    # Chuyển đổi string date thành date object
    route_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    daily_route = DailyRoute(
        route_id=route_id,
        date=route_date,
        fuel_cost=fuel_cost,
        fuel_quantity=fuel_quantity,
        fuel_price=fuel_price,
        trip_salary=trip_salary,
        notes=notes
    )
    db.add(daily_route)
    db.commit()
    return RedirectResponse(url="/daily", status_code=303)

@app.get("/salary", response_class=HTMLResponse)
async def salary_page(request: Request, db: Session = Depends(get_db), month: Optional[int] = None, year: Optional[int] = None):
    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    
    # Lấy tất cả nhân viên
    employees = db.query(Employee).all()
    
    # Tính lương cho từng nhân viên
    salary_data = []
    for employee in employees:
        # Lấy tất cả chuyến của nhân viên trong tháng
        daily_routes = db.query(DailyRoute).join(Route).filter(
            Route.employee_id == employee.id,
            DailyRoute.date >= date(year, month, 1),
            DailyRoute.date < date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        ).all()
        
        total_trip_salary = sum(dr.trip_salary for dr in daily_routes)
        total_fuel_cost = sum(dr.fuel_cost for dr in daily_routes)
        
        salary_data.append({
            'employee': employee,
            'base_salary': employee.base_salary,
            'trip_count': len(daily_routes),
            'total_trip_salary': total_trip_salary,
            'total_fuel_cost': total_fuel_cost,
            'total_salary': employee.base_salary + total_trip_salary
        })
    
    return templates.TemplateResponse("salary.html", {
        "request": request,
        "salary_data": salary_data,
        "month": month,
        "year": year
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

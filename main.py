from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
database = Database("sqlite:///users.db")
metadata = MetaData()

@app.on_event("startup")
async def startup():
    await database.connect()
    engine = create_engine(str(database.url))
    metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(request: Request):
    form = await request.form()
    csv_file = await form["file"].read()

    # Process the uploaded CSV file here
    # Map the Name and Age columns on the frontend

    return {"message": "CSV file uploaded successfully"}

@app.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    query = "SELECT * FROM users"
    result = await database.fetch_all(query)
    return templates.TemplateResponse("users.html", {"request": request, "users": result})

    import csv

@app.post("/upload")
async def upload(request: Request):
    form = await request.form()
    csv_file = await form["file"].read()

    # Process the uploaded CSV file here
    decoded_csv_file = csv_file.decode("utf-8")
    csv_data = csv.reader(decoded_csv_file.splitlines(), delimiter=",")
    for row in csv_data:
        name = row[0]  # Assuming Name is in the first column
        age = row[1]  # Assuming Age is in the second column

        # Save the data in the SQLite database here

    return {"message": "CSV file uploaded successfully"}

    users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("age", String),
)

@app.post("/upload")
async def upload(request: Request):
    form = await request.form()
    csv_file = await form["file"].read()

    decoded_csv_file = csv_file.decode("utf-8")
    csv_data = csv.reader(decoded_csv_file.splitlines(), delimiter=",")
    for row in csv_data:
        name = row[0]
        age = row[1]

        query = users.insert().values(name=name, age=age)
        await database.execute(query)

    return {"message": "CSV file uploaded successfully"}
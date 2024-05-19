from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import schemas

app = FastAPI()

host_name = "52.2.83.96"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_insurance2"  

# Obtener todos los siniestros
@app.get("/api/v1/claims")
def get_claims():
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM claims")
        result = cursor.fetchall()
        mydb.close()
        return {"claims": result}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un siniestro por ID
@app.get("/api/v1/claims/{id}")
def get_claim(id: int):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute(f"SELECT * FROM claims WHERE id = {id}")
        result = cursor.fetchone()
        mydb.close()
        if result:
            return {"claim": result}
        else:
            raise HTTPException(status_code=404, detail="Claim not found")
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agregar un nuevo siniestro
@app.post("/api/v1/claims")
def add_claim(item: schemas.Claim):
    if not all([item.claim_number, item.policy_number, item.description, item.amount, item.insured_person, item.date_of_incident, item.incident_location, item.date_filed, item.claim_status]):
        raise HTTPException(status_code=400, detail="All fields are required")

    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        sql = """INSERT INTO claims (claim_number, policy_number, description, amount, insured_person, date_of_incident, 
                 incident_location, date_filed, claim_status, adjuster_notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (item.claim_number, item.policy_number, item.description, item.amount, item.insured_person, item.date_of_incident, 
               item.incident_location, item.date_filed, item.claim_status, item.adjuster_notes)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return {"message": "Claim added successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar un siniestro
@app.put("/api/v1/claims/{id}")
def update_claim(id: int, item: schemas.Claim):
    if not all([item.claim_number, item.policy_number, item.description, item.amount, item.insured_person, item.date_of_incident, item.incident_location, item.date_filed, item.claim_status]):
        raise HTTPException(status_code=400, detail="All fields are required")
    
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        sql = """UPDATE claims set claim_number=%s, policy_number=%s, description=%s, amount=%s, insured_person=%s, 
                 date_of_incident=%s, incident_location=%s, date_filed=%s, claim_status=%s, adjuster_notes=%s where id=%s"""
        val = (item.claim_number, item.policy_number, item.description, item.amount, item.insured_person, item.date_of_incident, 
               item.incident_location, item.date_filed, item.claim_status, item.adjuster_notes, id)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return {"message": "Claim modified successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar un siniestro por ID
@app.delete("/api/v1/claims/{id}")
def delete_claim(id: int):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute(f"DELETE FROM claims WHERE id = {id}")
        mydb.commit()
        mydb.close()
        return {"message": "Claim deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

from flask import Flask, request, render_template
import joblib
import pandas as pd
import mysql.connector





# -------------------- APP INIT --------------------
app = Flask(__name__)


#-------------------- DB CONNECTION--------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shruti@2005",
    database="blood_bank"
)

cursor = db.cursor(dictionary=True)

# -------------------- LOAD MODEL --------------------
donor_model = joblib.load("donor_model.pkl")
model = joblib.load("shortage_model.pkl")
le_city = joblib.load("le_city.pkl")
le_group = joblib.load("le_group.pkl")


# -------------------- HOME ROUTE --------------------
@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        try:
            # Get form values
            city = request.form["city"]
            blood_group = request.form["blood_group"]
            thal_units = float(request.form["thalassemia_units_required"])

            # Encode categorical values
            city_enc = le_city.transform([city])[0]
            group_enc = le_group.transform([blood_group])[0]

            # Create dataframe for prediction
            features = pd.DataFrame(
                [[city_enc, group_enc, thal_units]],
                columns=["city", "blood_group", "thalassemia_units_required"]
            )

            # Predict
            pred = model.predict(features)[0]

            # Convert to message
            if pred == 1:
                prediction = "⚠️ High Risk of Blood Shortage"
            else:
                prediction = "✅ Blood Stock Available"

        except Exception as e:
            prediction = "Invalid input. Please check values."

    return render_template("index.html", prediction=prediction)
@app.route("/dashboard")
def dashboard(): 

    query = "SELECT city, blood_group, units_available FROM blood_stock"

    cursor.execute(query)

    data = cursor.fetchall()

    return render_template("dashboard.html",data=data)



@app.route("/donar_predict", methods=["GET", "POST"])
def donar():

    prediction = None

    if request.method == "POST":
        try:
            recency = float(request.form["recency"])
            frequency = float(request.form["frequency"])
            monetary = float(request.form["monetary"])
            time = float(request.form["time"])

            features = pd.DataFrame(
                [[recency, frequency, monetary, time]],
                columns=["Recency", "Frequency", "Monetary", "Time"]
            )


            

            pred = donor_model.predict(features)[0]

            

            print("Prediction value:", pred)
            #print(features)

            if pred == 1:
                prediction = "🩸 Likely to Donate "
            else:
                prediction = "❌ Not Likely to Donate "

        except Exception as e:
            print(e)
            prediction = "Invalid input!"

    return render_template("donar_predict.html", prediction=prediction)





@app.route("/register_donor", methods=["GET","POST"])
def register_donor():

    message = None

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        city = request.form["city"]
        phone = request.form["phone"]
        last_donation = request.form["last_donation"]

        query = """
        INSERT INTO donors (Name, age, blood_group, City, phone, last_donation_date)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query,(name,age,blood_group,city,phone,last_donation))
        db.commit()

        message = "Donor Registered Successfully!"

    return render_template("register_donor.html",message=message)





@app.route("/find_donor", methods=["GET","POST"])
def find_donor():

    donors = None
    message = None

    if request.method == "POST":

        city = request.form["city"]
        blood_group = request.form["blood_group"]

        query = """
        SELECT Name, age, blood_group, City, phone
        FROM donors
        WHERE City=%s AND blood_group=%s
        """

        cursor.execute(query,(city,blood_group))
        donors = cursor.fetchall()

        if not donors:
            message = "No matching donors available."


    return render_template("find_donor.html", donors=donors, message=message)





@app.route("/blood_request", methods=["GET","POST"])
def blood_request():

    message = None
    donors = None

    if request.method == "POST":

        city = request.form["city"]
        blood_group = request.form["blood_group"]
        units = int(request.form["units"])

        # Save request
        query = """
        INSERT INTO blood_requests (city,blood_group,units_required)
        VALUES (%s,%s,%s)
        """

        cursor.execute(query,(city,blood_group,units))
        db.commit()

        # Check stock
        stock_query = """
        SELECT units_available FROM blood_stock
        WHERE city=%s AND blood_group=%s
        """

        cursor.execute(stock_query,(city,blood_group))
        stock = cursor.fetchone()

        if stock and stock["units_available"] >= units:

            message = "Blood units available in stock."

        else:

            message = "Stock insufficient. Searching donors..."

            donor_query = """
            SELECT Name, phone, City
            FROM donors
            WHERE City=%s AND blood_group=%s
            """

            cursor.execute(donor_query,(city,blood_group))
            donors = cursor.fetchall()

    return render_template("blood_request.html",message=message,donors=donors)





@app.route("/blood_stock")
def blood_stock():

    cursor.execute("SELECT city,blood_group,units_available FROM blood_stock")

    data = cursor.fetchall()

    return render_template("blood_stock.html", data=data)




@app.route("/donor_list")
def donor_list():

    cursor.execute("SELECT * FROM donors")

    donors = cursor.fetchall()

    return render_template("donor_list.html", donors=donors)




@app.route("/requests")
def requests():

    cursor.execute("SELECT * FROM blood_requests")

    data = cursor.fetchall()

    return render_template("requests.html", data=data)
# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True)
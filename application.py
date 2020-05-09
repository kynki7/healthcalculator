from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if request.method == "POST":
        weight = request.form.get("weight")
        height = request.form.get("height")
        age = request.form.get("age")
        gender = request.form.get("gender")
        activity = request.form.get("activity")
        goal = request.form.get("goal")
        if not weight:
            print("enter weight")
            return false
        if not height:
            print("enter height")
            return false
        if not age:
            print("enter age")
            return false
        if not gender:
            print("enter gender")
            return false
        if not activity:
            print("enter activity")
            return false
        if not goal:
            print("enter goal")
            return false
            
        return redirect(url_for("stats"))
        
    else:
        return render_template("index.html")
        
@app.route("/stats", methods=["GET", "POST"])
def stats():
    
    if request.method == "POST":
        weight = int(request.form.get("weight"))
        height = int(request.form.get("height"))
        age = int(request.form.get("age"))
        gender = request.form.get("gender")
        activity = request.form.get("activity")
        goal = request.form.get("goal")        
        #Convert height to metres
        h = height / 100
        
        #Calculate BMI to 1 dp
        bmi = round((weight / (h * h)), 1)
        
        #Calculate BMR
        if gender == "male":
            bmr = round((66 + (13.7 * weight) + (5 * height) - (6.8 * age)))
        elif gender == "female":
            bmr = round((655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)))
        
        # Check risk level
        if bmi >= 18.5 and bmi <= 22.9:
            risk = "Low Risk"
        elif bmi >= 23 and bmi <= 27.4:
            risk = "Moderate Risk"
        elif bmi >= 27.5:
            risk = "High Risk"
        else:
            risk = "Invalid BMI, input appropriate numbers"
            
        #Calculate TDEE
        if activity == "low":
            tdee = round(1.2 * bmr)
        elif activity == "medium":
            tdee = round(1.53 * bmr)
        elif activity == "high":
            tdee = round(1.88 * bmr)
        
        #Sort out macros
        if goal == "lw":
            total_calories = round(tdee * 0.85)
            protein = round(2.3 * weight)
            remaining_calories = total_calories - (protein * 4)
            carbs = round(((0.63 * remaining_calories) / 4))
            fat = round(((0.37 * remaining_calories) / 9))
        elif goal == "gm":
            total_calories = round(tdee * 1.1)
            protein = round(1.6 * weight)
            remaining_calories = total_calories - (protein * 4)
            carbs = round(((0.63 * remaining_calories) / 4))
            fat = round(((0.37 * remaining_calories) / 9))
        elif goal == "mm":
            total_calories = round(tdee)
            protein = round(0.8 * weight)
            remaining_calories = total_calories - (protein * 4)
            carbs = round(((0.63 * remaining_calories) / 4))
            fat = round(((0.37 * remaining_calories) / 9))
            
        return render_template("stats.html", bmi=bmi, bmr=bmr, tdee=tdee, 
                                total_calories=total_calories, risk=risk, 
                                protein=protein, carbs=carbs, fat=fat)
                                
    else:
        return render_template("index.html")
    

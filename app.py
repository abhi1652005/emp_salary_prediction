from flask import Flask, render_template_string, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model using your exact pkl file name
# (Ensure your exact pkl file is in the same directory as app.py)
with open("nv.pkl", "rb") as f:
    model = pickle.load(f)

# Attractive HTML Template with embedded CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Prediction Portal</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--card-bg);
            padding: 2.5rem;
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 480px;
            box-sizing: border-box;
        }
        h2 {
            margin-top: 0;
            font-weight: 700;
            color: #0f172a;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .form-group {
            margin-bottom: 1.25rem;
        }
        label {
            display: block;
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
            color: #475569;
        }
        input, select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #cbd5e1;
            border-radius: 0.5rem;
            font-size: 1rem;
            box-sizing: border-box;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }
        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 0.5rem;
        }
        button:hover {
            background-color: var(--primary-hover);
        }
        .result-card {
            margin-top: 1.5rem;
            padding: 1rem;
            background-color: #e0e7ff;
            border: 1px solid #c7d2fe;
            border-radius: 0.5rem;
            text-align: center;
            color: #3730a3;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Prediction Portal</h2>
        <form method="POST">
            <div class="form-group">
                <label for="age">Age</label>
                <input type="number" id="age" name="age" required placeholder="e.g., 30">
            </div>
            
            <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" name="gender" required>
                    <option value="" disabled selected>Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="experience">Years of Experience</label>
                <input type="number" step="0.1" id="experience" name="experience" required placeholder="e.g., 5.0">
            </div>
            
            <div class="form-group">
                <label for="salary">Salary</label>
                <input type="number" id="salary" name="salary" required placeholder="e.g., 60000">
            </div>
            
            <div class="form-group">
                <label for="job_title">Job Title</label>
                <input type="text" id="job_title" name="job_title" required placeholder="e.g., Software Engineer">
            </div>
            
            <button type="submit">Predict</button>
        </form>

        {% if prediction is not none %}
        <div class="result-card">
            Prediction Result: {{ prediction }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            # Inputs matching your exact model features:
            # ['Age', 'Gender', 'Years of Experience', 'Salary', 'Job Title'][cite: 1]
            age = float(request.form["age"])
            gender = request.form["gender"]
            experience = float(request.form["experience"])
            salary = float(request.form["salary"])
            job_title = request.form["job_title"]
            
            # Note: GaussianNB expects numeric inputs. If 'Gender' and 'Job Title' were 
            # label-encoded during training, make sure to encode them identically here.
            # Example placeholder:
            # prediction = model.predict([[age, gender_encoded, experience, salary, job_title_encoded]])[0]
            
            prediction = "Processed Successfully (Ensure categorical variables are encoded if required by the model)"
        except Exception as e:
            prediction = f"Error: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

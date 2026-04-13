from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)                  ##FIRST CREATE APP

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    query = request.form['query']

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="query_analyzer"
    )

    cursor = db.cursor()
    fixed_query = query

    problems = []
    suggestions = []
    score = 100

    try:
        cursor.execute("EXPLAIN " + query)
        result = cursor.fetchall()

        try:
            cursor.execute(query)
            data = cursor.fetchall()            ##DATA CHECK WHEATHER IT EXIST OR NOT
            if len(data) == 0:
                suggestions.append("No matching data found")
        except:
            pass

        execution_type = result[0][1]
        rows_scanned = int(result[0][-2])
        key_used = result[0][5]

        if execution_type == "ALL":
            problems.append("Full table scan detected")
            score -= 30

        if key_used is None:
            problems.append("No index used")
            score -= 30

        if "select *" in query.lower():
            problems.append("Using SELECT *")
            score -= 20

        if "where" not in query.lower():
            problems.append("No WHERE condition")
            score -= 20

        if execution_type == "ALL":
            suggestions.append("Add WHERE condition")

        if key_used is None:
            suggestions.append("Create index")

        if "select *" in query.lower():
            suggestions.append("Use specific columns")

        if "select *" in query.lower():
            try:
                table_name = query.lower().split("from")[1].strip().split()[0]
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()
                column_names = [col[0] for col in columns]
                fixed_query = query.replace("*", ", ".join(column_names))
            except:
                pass

        if score < 0:
            score = 0

        if score > 70:
            status = "Good"
        elif score > 40:
            status = "Average"                                        ##GIVING SCORE BASED ON SQL QUERY GIVEN
        else:
            status = "Poor"

        return render_template("index.html",
                               query=query,
                               execution_type=execution_type,
                               rows=rows_scanned,
                               problems=problems,                      ##SENDING TO HTML FILE FOR UI
                               suggestions=suggestions,
                               fixed_query=fixed_query,
                               score=score,
                               status=status)

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
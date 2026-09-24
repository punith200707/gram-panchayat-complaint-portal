from flask import Flask, request, redirect, url_for, session, send_from_directory
import sqlite3
import uuid
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "gram_panchayat_portal_2026"

DATABASE = "water_complaints.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            complaint_id TEXT UNIQUE NOT NULL,

            name TEXT NOT NULL,

            mobile TEXT NOT NULL,

            village TEXT NOT NULL,

            water_problem TEXT NOT NULL,

            description TEXT NOT NULL,

            photo TEXT,

            status TEXT DEFAULT 'Submitted',

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# PAGE START
# ============================================================

def page_start(title):

    return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>{title}</title>


<style>

/* ============================================================
   GENERAL
============================================================ */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        Arial,
        "Noto Sans Kannada",
        sans-serif;

    background: #f3f8fc;

    color: #17324d;
}}


/* ============================================================
   HEADER
============================================================ */

header {{

    background: #075985;

    color: white;

    padding: 18px 6%;

    display: flex;

    justify-content: space-between;

    align-items: center;

    flex-wrap: wrap;

    gap: 15px;
}}


.logo {{

    font-size: 23px;

    font-weight: bold;
}}


nav {{

    display: flex;

    align-items: center;

    gap: 8px;

    flex-wrap: wrap;
}}


nav a {{

    color: white;

    text-decoration: none;

    padding: 9px 11px;

    border-radius: 5px;
}}


nav a:hover {{

    background: #0369a1;
}}


/* ============================================================
   LANGUAGE BUTTON
============================================================ */

.language-btn {{

    background: #fbbf24;

    color: #111827;

    border: none;

    padding: 10px 15px;

    border-radius: 6px;

    font-weight: bold;

    cursor: pointer;

    font-size: 14px;
}}


.language-btn:hover {{

    background: #f59e0b;
}}


/* ============================================================
   HERO
============================================================ */

.hero {{

    background:
        linear-gradient(
            135deg,
            #075985,
            #0284c7
        );

    color: white;

    text-align: center;

    padding: 75px 20px;
}}


.water-icon {{

    font-size: 70px;
}}


.hero h1 {{

    font-size: 48px;

    margin: 12px 0 5px 0;
}}


.hero h2 {{

    font-size: 27px;

    margin: 5px 0 20px 0;

    font-weight: normal;
}}


.hero p {{

    max-width: 750px;

    margin: 15px auto;

    font-size: 19px;

    line-height: 1.7;
}}


/* ============================================================
   BUTTON
============================================================ */

.button {{

    display: inline-block;

    background: #0284c7;

    color: white;

    border: none;

    padding: 13px 23px;

    border-radius: 7px;

    text-decoration: none;

    font-size: 16px;

    font-weight: bold;

    cursor: pointer;

    margin: 5px;
}}


.button:hover {{

    background: #0369a1;
}}


.green {{

    background: #0f766e;
}}


.green:hover {{

    background: #115e59;
}}


/* ============================================================
   CONTAINER
============================================================ */

.container {{

    max-width: 850px;

    margin: 45px auto;

    padding: 20px;
}}


/* ============================================================
   BOX
============================================================ */

.box {{

    background: white;

    padding: 35px;

    border-radius: 12px;

    box-shadow:
        0 4px 20px
        rgba(0,0,0,0.08);
}}


.box h1 {{

    margin-top: 0;
}}


/* ============================================================
   FORM
============================================================ */

label {{

    display: block;

    margin-top: 17px;

    margin-bottom: 7px;

    font-weight: bold;
}}


input,
select,
textarea {{

    width: 100%;

    padding: 13px;

    border:
        1px solid
        #cbd5e1;

    border-radius: 6px;

    font-size: 16px;

    font-family: inherit;
}}


input:focus,
select:focus,
textarea:focus {{

    outline: none;

    border-color: #0284c7;
}}


textarea {{

    resize: vertical;
}}


.full-button {{

    width: 100%;

    margin-top: 22px;
}}


/* ============================================================
   PHOTO UPLOAD
============================================================ */

.photo-help {{

    background: #e0f2fe;

    padding: 15px;

    margin-top: 10px;

    border-radius: 7px;

    font-size: 14px;

    color: #075985;

    line-height: 1.6;
}}


/* ============================================================
   INFORMATION CARDS
============================================================ */

.info-section {{

    text-align: center;

    padding: 45px 20px;
}}


.info-cards {{

    display: flex;

    justify-content: center;

    gap: 20px;

    flex-wrap: wrap;
}}


.info-card {{

    background: white;

    width: 250px;

    padding: 25px;

    border-radius: 10px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,0.07);
}}


.info-card .icon {{

    font-size: 45px;
}}


/* ============================================================
   SUCCESS
============================================================ */

.success {{

    text-align: center;

    border-top:
        5px solid
        #0f766e;
}}


.complaint-id {{

    display: inline-block;

    background: #e0f2fe;

    color: #0369a1;

    padding: 15px 25px;

    border-radius: 8px;

    font-size: 28px;

    font-weight: bold;

    margin: 15px;
}}


/* ============================================================
   RESULT
============================================================ */

.result {{

    margin-top: 30px;

    background: #eff6ff;

    border-left:
        5px solid
        #0284c7;

    padding: 25px;

    border-radius: 8px;
}}


.result-row {{

    padding: 13px 0;

    border-bottom:
        1px solid
        #dbeafe;
}}


.status {{

    display: inline-block;

    background: #0f766e;

    color: white;

    padding: 7px 13px;

    border-radius: 20px;

    font-weight: bold;
}}


.alert {{

    max-width: 850px;

    margin: 20px auto;

    padding: 15px;

    background: #fee2e2;

    color: #991b1b;

    border-radius: 7px;

    text-align: center;

    font-weight: bold;
}}


/* ============================================================
   PHOTO DISPLAY
============================================================ */

.complaint-photo {{

    max-width: 100%;

    max-height: 400px;

    border-radius: 10px;

    margin-top: 12px;

    border:
        2px solid
        #dbeafe;
}}


/* ============================================================
   ADMIN
============================================================ */

.admin {{

    padding: 35px 5%;
}}


.admin-top {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    flex-wrap: wrap;

    gap: 15px;
}}


.logout {{

    background: #dc2626;
}}


.logout:hover {{

    background: #b91c1c;
}}


.table-container {{

    margin-top: 30px;

    overflow-x: auto;

    background: white;

    border-radius: 10px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,0.05);
}}


table {{

    width: 100%;

    border-collapse: collapse;

    min-width: 1300px;
}}


th {{

    background: #075985;

    color: white;

    padding: 13px;

    text-align: left;
}}


td {{

    padding: 13px;

    border-bottom:
        1px solid
        #ddd;

    vertical-align: top;
}}


.update-form {{

    display: flex;

    gap: 5px;
}}


.update-form select {{

    width: 150px;

    padding: 8px;
}}


.update-form button {{

    background: #0284c7;

    color: white;

    border: none;

    padding: 8px 12px;

    border-radius: 5px;

    cursor: pointer;
}}


.admin-photo {{

    width: 130px;

    height: 100px;

    object-fit: cover;

    border-radius: 8px;

    border:
        2px solid
        #dbeafe;
}}


/* ============================================================
   DEMO LOGIN
============================================================ */

.demo {{

    margin-top: 25px;

    padding: 15px;

    background: #fef3c7;

    border-radius: 7px;

    text-align: center;
}}


/* ============================================================
   FOOTER
============================================================ */

footer {{

    background: #075985;

    color: white;

    text-align: center;

    padding: 25px;

    margin-top: 40px;
}}


/* ============================================================
   LANGUAGE
============================================================ */

.kannada {{

    display: none;
}}


/* ============================================================
   MOBILE
============================================================ */

@media(max-width:700px) {{

    header {{

        justify-content: center;

        text-align: center;
    }}

    .hero h1 {{

        font-size: 34px;
    }}

    .hero h2 {{

        font-size: 22px;
    }}

    .hero p {{

        font-size: 17px;
    }}

    .box {{

        padding: 25px 18px;
    }}

    .container {{

        margin: 20px auto;
    }}

}}

</style>


<script>

/* ============================================================
   LANGUAGE SWITCH
============================================================ */

let kannadaMode = false;


function changeLanguage() {{

    kannadaMode = !kannadaMode;


    const english =
        document.querySelectorAll(".english");


    const kannada =
        document.querySelectorAll(".kannada");


    english.forEach(function(element) {{

        element.style.display =
            kannadaMode
            ? "none"
            : "inline";

    }});


    kannada.forEach(function(element) {{

        element.style.display =
            kannadaMode
            ? "inline"
            : "none";

    }});

}}

</script>

</head>


<body>


<!-- ========================================================
     HEADER
========================================================= -->

<header>


<div class="logo">

🏛️

<span class="english">
Gram Panchayat Portal
</span>

<span class="kannada">
ಗ್ರಾಮ ಪಂಚಾಯಿತಿ ಪೋರ್ಟಲ್
</span>

</div>


<nav>


<a href="/">

<span class="english">
Home
</span>

<span class="kannada">
ಮುಖಪುಟ
</span>

</a>


<a href="/submit">

<span class="english">
Water Complaint
</span>

<span class="kannada">
ನೀರಿನ ದೂರು
</span>

</a>


<a href="/track">

<span class="english">
Track Complaint
</span>

<span class="kannada">
ದೂರು ಪರಿಶೀಲಿಸಿ
</span>

</a>


<a href="/login">

<span class="english">
Admin
</span>

<span class="kannada">
ನಿರ್ವಾಹಕ
</span>

</a>


<button
    class="language-btn"
    onclick="changeLanguage()">

ಕನ್ನಡ / English

</button>


</nav>

</header>


<main>

"""


# ============================================================
# PAGE END
# ============================================================

def page_end():

    return """

</main>


<footer>

<p>
🏛️ Gram Panchayat Portal
</p>

<p>
💧 Water Complaint Service
</p>

<p>
© 2026 Gram Panchayat
</p>

</footer>


</body>

</html>

"""


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    html = page_start(
        "Gram Panchayat Portal"
    )


    html += """

<section class="hero">


<div class="water-icon">
🏛️
</div>


<h1 class="english">
Gram Panchayat Portal
</h1>


<h1 class="kannada">
ಗ್ರಾಮ ಪಂಚಾಯಿತಿ ಪೋರ್ಟಲ್
</h1>


<h2 class="english">
Water Complaint Portal
</h2>


<h2 class="kannada">
ನೀರಿನ ದೂರು ಪೋರ್ಟಲ್
</h2>


<p class="english">

Report water supply problems in your village,
upload a photo, and track your complaint online.

</p>


<p class="kannada">

ನಿಮ್ಮ ಗ್ರಾಮದ ನೀರು ಸರಬರಾಜಿನ ಸಮಸ್ಯೆಗಳನ್ನು
ವರದಿ ಮಾಡಿ, ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ
ಮತ್ತು ನಿಮ್ಮ ದೂರನ್ನು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.

</p>


<br>


<a
    href="/submit"
    class="button">

<span class="english">
📝 Report Water Problem
</span>

<span class="kannada">
📝 ನೀರಿನ ಸಮಸ್ಯೆ ವರದಿ ಮಾಡಿ
</span>

</a>


<a
    href="/track"
    class="button green">

<span class="english">
🔎 Track Complaint
</span>

<span class="kannada">
🔎 ದೂರು ಪರಿಶೀಲಿಸಿ
</span>

</a>


</section>


<!-- ========================================================
     SERVICE CARDS
========================================================= -->

<section class="info-section">


<h2 class="english">
Water Complaint Services
</h2>


<h2 class="kannada">
ನೀರಿನ ದೂರು ಸೇವೆಗಳು
</h2>


<div class="info-cards">


<div class="info-card">

<div class="icon">
🚱
</div>

<h3 class="english">
No Water Supply
</h3>

<h3 class="kannada">
ನೀರು ಸರಬರಾಜು ಇಲ್ಲ
</h3>

<p class="english">
Report when water is not reaching your area.
</p>

<p class="kannada">
ನಿಮ್ಮ ಪ್ರದೇಶಕ್ಕೆ ನೀರು ಬರುತ್ತಿಲ್ಲದಿದ್ದರೆ ದೂರು ನೀಡಿ.
</p>

</div>


<div class="info-card">

<div class="icon">
💧
</div>

<h3 class="english">
Low Water Supply
</h3>

<h3 class="kannada">
ಕಡಿಮೆ ನೀರು ಸರಬರಾಜು
</h3>

<p class="english">
Report low or irregular water supply.
</p>

<p class="kannada">
ಕಡಿಮೆ ಅಥವಾ ಅನಿಯಮಿತ ನೀರು ಸರಬರಾಜಿನ ಬಗ್ಗೆ ದೂರು ನೀಡಿ.
</p>

</div>


<div class="info-card">

<div class="icon">
📷
</div>

<h3 class="english">
Upload Photo
</h3>

<h3 class="kannada">
ಫೋಟೋ ಅಪ್‌ಲೋಡ್
</h3>

<p class="english">
Upload a photo showing the water problem.
</p>

<p class="kannada">
ನೀರಿನ ಸಮಸ್ಯೆಯನ್ನು ತೋರಿಸುವ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.
</p>

</div>


</div>

</section>

"""


    html += page_end()

    return html


# ============================================================
# SUBMIT WATER COMPLAINT
# ============================================================

@app.route(
    "/submit",
    methods=["GET", "POST"]
)
def submit():


    if request.method == "POST":


        name = request.form.get(
            "name",
            ""
        ).strip()


        mobile = request.form.get(
            "mobile",
            ""
        ).strip()


        village = request.form.get(
            "village",
            ""
        ).strip()


        water_problem = request.form.get(
            "water_problem",
            ""
        ).strip()


        description = request.form.get(
            "description",
            ""
        ).strip()


        photo = request.files.get(
            "photo"
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not name or not mobile or not village:

            return """

<script>

alert(
    "Please fill all required fields."
);

window.history.back();

</script>

"""


        # ----------------------------------------------------
        # PHOTO
        # ----------------------------------------------------

        filename = None


        if photo and photo.filename:


            extension = os.path.splitext(
                photo.filename
            )[1].lower()


            allowed_extensions = [

                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"

            ]


            if extension not in allowed_extensions:

                return """

<script>

alert(
    "Only JPG, JPEG, PNG, GIF and WEBP images are allowed."
);

window.history.back();

</script>

"""


            filename = (
                uuid.uuid4().hex
                + extension
            )


            photo.save(

                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

            )


        # ----------------------------------------------------
        # COMPLAINT ID
        # ----------------------------------------------------

        complaint_id = (

            "WATER-"
            + uuid.uuid4().hex[:8].upper()

        )


        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ----------------------------------------------------
        # SAVE DATABASE
        # ----------------------------------------------------

        conn = get_db()


        conn.execute("""
            INSERT INTO complaints
            (
                complaint_id,
                name,
                mobile,
                village,
                water_problem,
                description,
                photo,
                status,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            complaint_id,

            name,

            mobile,

            village,

            water_problem,

            description,

            filename,

            "Submitted",

            created_at

        ))


        conn.commit()

        conn.close()


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        html = page_start(
            "Complaint Submitted"
        )


        html += f"""

<div class="container">


<div class="box success">


<h1 class="english">

Water Complaint Submitted Successfully! ✅

</h1>


<h1 class="kannada">

ನೀರಿನ ದೂರು ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ! ✅

</h1>


<p class="english">

Your Complaint ID is:

</p>


<p class="kannada">

ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆ:

</p>


<div class="complaint-id">

{complaint_id}

</div>


<p class="english">

Please save this ID to track your complaint.

</p>


<p class="kannada">

ನಿಮ್ಮ ದೂರನ್ನು ಪರಿಶೀಲಿಸಲು ಈ ಸಂಖ್ಯೆಯನ್ನು ಉಳಿಸಿಕೊಳ್ಳಿ.

</p>


<a
    href="/track"
    class="button">

🔎 Track Complaint

</a>


<br>


<a
    href="/submit"
    class="button green">

Submit Another Complaint

</a>


</div>

</div>

"""


        html += page_end()


        return html


    # ========================================================
    # FORM
    # ========================================================

    html = page_start(
        "Water Complaint"
    )


    html += """

<div class="container">


<div class="box">


<h1 class="english">

💧 Water Complaint Portal

</h1>


<h1 class="kannada">

💧 ನೀರಿನ ದೂರು ಪೋರ್ಟಲ್

</h1>


<p class="english">

Submit your water-related complaint.

</p>


<p class="kannada">

ನಿಮ್ಮ ನೀರಿಗೆ ಸಂಬಂಧಿಸಿದ ದೂರನ್ನು ಸಲ್ಲಿಸಿ.

</p>


<form
    method="POST"
    enctype="multipart/form-data">


<!-- NAME -->

<label>

Name / ಹೆಸರು

</label>


<input
    type="text"
    name="name"
    placeholder="Enter your name / ನಿಮ್ಮ ಹೆಸರು"
    required
>


<!-- MOBILE -->

<label>

Mobile Number / ಮೊಬೈಲ್ ಸಂಖ್ಯೆ

</label>


<input
    type="tel"
    name="mobile"
    placeholder="Enter mobile number / ಮೊಬೈಲ್ ಸಂಖ್ಯೆ"
    required
>


<!-- VILLAGE -->

<label>

Village / ಗ್ರಾಮ

</label>


<input
    type="text"
    name="village"
    placeholder="Enter village name / ಗ್ರಾಮದ ಹೆಸರು"
    required
>


<!-- WATER PROBLEM -->

<label>

Water Problem / ನೀರಿನ ಸಮಸ್ಯೆ

</label>


<select
    name="water_problem"
    required>


<option value="">

Select Problem /
ಸಮಸ್ಯೆ ಆಯ್ಕೆಮಾಡಿ

</option>


<option value="No Water Supply">

🚱 No Water Supply /
ನೀರು ಸರಬರಾಜು ಇಲ್ಲ

</option>


<option value="Low Water Supply">

💧 Low Water Supply /
ಕಡಿಮೆ ನೀರು ಸರಬರಾಜು

</option>


<option value="Irregular Water Supply">

⏰ Irregular Water Supply /
ಅನಿಯಮಿತ ನೀರು ಸರಬರಾಜು

</option>


<option value="Dirty Water">

🧪 Dirty Water /
ಕಲುಷಿತ ನೀರು

</option>


<option value="Water Leakage">

💦 Water Leakage /
ನೀರು ಸೋರಿಕೆ

</option>


<option value="Other Water Problem">

❗ Other Water Problem /
ಇತರೆ ನೀರಿನ ಸಮಸ್ಯೆ

</option>


</select>


<!-- DESCRIPTION -->

<label>

Description / ದೂರು ವಿವರ

</label>


<textarea
    name="description"
    rows="6"
    placeholder="Describe the water problem / ನೀರಿನ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ"
    required
></textarea>


<!-- PHOTO -->

<label>

📷 Photo / ಫೋಟೋ

</label>


<input
    type="file"
    name="photo"
    accept="image/*"
>


<div class="photo-help">


<strong>
📷 Photo Upload / ಫೋಟೋ ಅಪ್‌ಲೋಡ್
</strong>


<br><br>


<span class="english">

You can upload a photo showing the water problem.

Maximum file size: 5 MB.

Supported formats:
JPG, JPEG, PNG, GIF, WEBP.

</span>


<span class="kannada">

ನೀರಿನ ಸಮಸ್ಯೆಯನ್ನು ತೋರಿಸುವ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಬಹುದು.

ಗರಿಷ್ಠ ಫೈಲ್ ಗಾತ್ರ: 5 MB.

JPG, JPEG, PNG, GIF, WEBP ಸ್ವರೂಪಗಳನ್ನು ಬೆಂಬಲಿಸಲಾಗುತ್ತದೆ.

</span>


</div>


<!-- SUBMIT -->

<button
    type="submit"
    class="button full-button">


<span class="english">

💧 Submit Water Complaint

</span>


<span class="kannada">

💧 ನೀರಿನ ದೂರು ಸಲ್ಲಿಸಿ

</span>


</button>


</form>


</div>

</div>

"""


    html += page_end()


    return html


# ============================================================
# SERVE PHOTOS
# ============================================================

@app.route(
    "/uploads/<filename>"
)
def uploaded_file(filename):

    return send_from_directory(

        UPLOAD_FOLDER,

        filename

    )


# ============================================================
# TRACK COMPLAINT
# ============================================================

@app.route(
    "/track",
    methods=["GET", "POST"]
)
def track():


    complaint = None

    error = None


    if request.method == "POST":


        complaint_id = request.form.get(
            "complaint_id",
            ""
        ).strip().upper()


        conn = get_db()


        complaint = conn.execute("""

            SELECT *

            FROM complaints

            WHERE complaint_id = ?

        """, (

            complaint_id,

        )).fetchone()


        conn.close()


        if complaint is None:

            error = "Complaint not found."


    html = page_start(
        "Track Water Complaint"
    )


    html += """

<div class="container">


<div class="box">


<h1 class="english">

🔎 Track Water Complaint

</h1>


<h1 class="kannada">

🔎 ನೀರಿನ ದೂರು ಪರಿಶೀಲಿಸಿ

</h1>


<p class="english">

Enter your Complaint ID to check the current status.

</p>


<p class="kannada">

ಪ್ರಸ್ತುತ ಸ್ಥಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಲು ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.

</p>


<form method="POST">


<label>

Complaint ID / ದೂರು ಸಂಖ್ಯೆ

</label>


<input
    type="text"
    name="complaint_id"
    placeholder="Example: WATER-1234ABCD"
    required
>


<button
    type="submit"
    class="button full-button">

🔎 Track / ಪರಿಶೀಲಿಸಿ

</button>


</form>

"""


    if error:


        html += """

<div class="alert">

❌ Complaint not found.

<br>

ದೂರು ಕಂಡುಬಂದಿಲ್ಲ.

</div>

"""


    if complaint:


        photo_html = ""


        if complaint["photo"]:


            photo_html = f"""

<div class="result-row">


<strong>

📷 Complaint Photo /
ದೂರು ಫೋಟೋ

</strong>


<br>


<img
    class="complaint-photo"
    src="/uploads/{complaint["photo"]}"
    alt="Complaint Photo"
>


</div>

"""


        html += f"""

<div class="result">


<h2>

💧 {complaint["complaint_id"]}

</h2>


<div class="result-row">

<strong>
Name / ಹೆಸರು
</strong>

<br>

{complaint["name"]}

</div>


<div class="result-row">

<strong>
Mobile / ಮೊಬೈಲ್
</strong>

<br>

{complaint["mobile"]}

</div>


<div class="result-row">

<strong>
Village / ಗ್ರಾಮ
</strong>

<br>

{complaint["village"]}

</div>


<div class="result-row">

<strong>
Water Problem / ನೀರಿನ ಸಮಸ್ಯೆ
</strong>

<br>

{complaint["water_problem"]}

</div>


<div class="result-row">

<strong>
Description / ವಿವರ
</strong>

<br>

{complaint["description"]}

</div>


{photo_html}


<div class="result-row">

<strong>
Status / ಸ್ಥಿತಿ
</strong>

<br><br>


<span class="status">

{complaint["status"]}

</span>


</div>


<div class="result-row">

<strong>
Submitted / ಸಲ್ಲಿಸಿದ ದಿನಾಂಕ
</strong>

<br>

{complaint["created_at"]}

</div>


</div>

"""


    html += """

</div>

</div>

"""


    html += page_end()


    return html


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():


    error = ""


    if request.method == "POST":


        username = request.form.get(
            "username"
        )


        password = request.form.get(
            "password"
        )


        if (

            username == ADMIN_USERNAME

            and

            password == ADMIN_PASSWORD

        ):


            session["admin"] = True


            return redirect(
                url_for("admin")
            )


        error = "Invalid username or password."


    html = page_start(
        "Gram Panchayat Admin"
    )


    html += f"""

<div class="container">


<div class="box">


<h1 class="english">

🔐 Gram Panchayat Admin Login

</h1>


<h1 class="kannada">

🔐 ಗ್ರಾಮ ಪಂಚಾಯಿತಿ ನಿರ್ವಾಹಕ ಲಾಗಿನ್

</h1>


"""


    if error:


        html += f"""

<div class="alert">

❌ {error}

</div>

"""


    html += """

<form method="POST">


<label>

Username / ಬಳಕೆದಾರ ಹೆಸರು

</label>


<input
    type="text"
    name="username"
    required
>


<label>

Password / ಪಾಸ್‌ವರ್ಡ್

</label>


<input
    type="password"
    name="password"
    required
>


<button
    type="submit"
    class="button full-button">

Login / ಲಾಗಿನ್

</button>


</form>


<div class="demo">


<strong>

Demo Admin Login

</strong>


<p>

Username:

<b>
admin
</b>

</p>


<p>

Password:

<b>
admin123
</b>

</p>


</div>


</div>

</div>

"""


    html += page_end()


    return html


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
def admin():


    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    conn = get_db()


    complaints = conn.execute("""

        SELECT *

        FROM complaints

        ORDER BY id DESC

    """).fetchall()


    conn.close()


    html = page_start(
        "Gram Panchayat Admin Dashboard"
    )


    html += f"""

<div class="admin">


<div class="admin-top">


<div>


<h1>

🏛️ Gram Panchayat Portal

</h1>


<h2>

💧 Water Complaint Dashboard

</h2>


<p>

Total Water Complaints /

ಒಟ್ಟು ನೀರಿನ ದೂರುಗಳು:

<strong>

{len(complaints)}

</strong>

</p>


</div>


<a
    href="/logout"
    class="button logout">

Logout / ಲಾಗ್‌ಔಟ್

</a>


</div>


<div class="table-container">


<table>


<thead>


<tr>


<th>
Complaint ID
</th>


<th>
Name
</th>


<th>
Mobile
</th>


<th>
Village
</th>


<th>
Water Problem
</th>


<th>
Description
</th>


<th>
Photo
</th>


<th>
Status
</th>


<th>
Update
</th>


</tr>


</thead>


<tbody>

"""


    if len(complaints) == 0:


        html += """

<tr>


<td
    colspan="9"
    style="
        text-align:center;
        padding:40px;
    ">


No water complaints available.


<br><br>


ಯಾವುದೇ ನೀರಿನ ದೂರುಗಳು ಲಭ್ಯವಿಲ್ಲ.


</td>


</tr>

"""


    for complaint in complaints:


        photo_html = "No Photo"


        if complaint["photo"]:


            photo_html = f"""

<a
    href="/uploads/{complaint["photo"]}"
    target="_blank">


<img
    class="admin-photo"
    src="/uploads/{complaint["photo"]}"
    alt="Complaint Photo">


</a>

"""


        statuses = [

            "Submitted",

            "Under Review",

            "In Progress",

            "Resolved",

            "Rejected"

        ]


        options = ""


        for status in statuses:


            selected = ""


            if complaint["status"] == status:

                selected = "selected"


            options += f"""

<option
    value="{status}"
    {selected}>

{status}

</option>

"""


        html += f"""

<tr>


<td>

<strong>

{complaint["complaint_id"]}

</strong>

</td>


<td>

{complaint["name"]}

</td>


<td>

{complaint["mobile"]}

</td>


<td>

{complaint["village"]}

</td>


<td>

{complaint["water_problem"]}

</td>


<td>

{complaint["description"]}

</td>


<td>

{photo_html}

</td>


<td>


<span class="status">

{complaint["status"]}

</span>


</td>


<td>


<form
    method="POST"
    action="/update/{complaint["id"]}"
    class="update-form">


<select name="status">

{options}

</select>


<button type="submit">

Update

</button>


</form>


</td>


</tr>

"""


    html += """

</tbody>

</table>

</div>

</div>

"""


    html += page_end()


    return html


# ============================================================
# UPDATE COMPLAINT STATUS
# ============================================================

@app.route(
    "/update/<int:complaint_id>",
    methods=["POST"]
)
def update_status(complaint_id):


    if not session.get("admin"):

        return redirect(
            url_for("login")
        )


    status = request.form.get(
        "status"
    )


    allowed = [

        "Submitted",

        "Under Review",

        "In Progress",

        "Resolved",

        "Rejected"

    ]


    if status not in allowed:

        return redirect(
            url_for("admin")
        )


    conn = get_db()


    conn.execute("""

        UPDATE complaints

        SET status = ?

        WHERE id = ?

    """, (

        status,

        complaint_id

    ))


    conn.commit()

    conn.close()


    return redirect(
        url_for("admin")
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":


    create_database()


    print("")
    print("==============================================")
    print("       GRAM PANCHAYAT PORTAL")
    print("       WATER COMPLAINT SERVICE")
    print("==============================================")
    print("")
    print("Open this address in your browser:")
    print("")
    print("http://127.0.0.1:5000")
    print("")
    print("ADMIN LOGIN")
    print("Username: admin")
    print("Password: admin123")
    print("")
    print("Photo upload limit: 5 MB")
    print("")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )


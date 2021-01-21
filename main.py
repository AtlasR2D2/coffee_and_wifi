from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pandas as pd
import datetime

COFFEE_EMOJI = "☕"
WIFI_EMOJI = "💪"
NOT_AVAILABLE_EMOJI = "✘"
POWER_EMOJI = "🔌"
MAX_STARS = 5


def generate_stars(star_icon, num: int):
    """Generates a concatenated string of num star icons"""
    star_string = ""
    if num == 0:
        star_string = NOT_AVAILABLE_EMOJI
    else:
        for i in range(num):
            star_string += star_icon
    # Output String
    return star_string

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), URL()])
    open_time = TimeField("What time does the cafe open (HH:MM)?", validators=[DataRequired()])
    closing_time = TimeField("What time does the cafe close (HH:MM)?", validators=[DataRequired()])
    coffee_rating = SelectField(choices=[generate_stars(COFFEE_EMOJI, num) for num in range(MAX_STARS+1)], validators=[DataRequired()])
    wifi_rating = SelectField(choices=[generate_stars(WIFI_EMOJI, num) for num in range(MAX_STARS + 1)], validators=[DataRequired()])
    power_rating = SelectField(choices=[generate_stars(POWER_EMOJI, num) for num in range(MAX_STARS + 1)], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    cafe_details = []
    if form.validate_on_submit():
        # Add Cafe Details to data store csv
        cafe_details.append(form.cafe.data)
        cafe_details.append(form.location_url.data)
        cafe_details.append(form.open_time.data.strftime("HH:MM"))
        cafe_details.append(form.closing_time.data.strftime("HH:MM"))
        cafe_details.append(form.coffee_rating.data)
        cafe_details.append(form.wifi_rating.data)
        cafe_details.append(form.power_rating.data)
        print(cafe_details)
        with open("./cafe-data.csv", mode="a", encoding="utf-8") as cafe_csv:
            cafe_csv.write("\n"+", ".join(cafe_details))
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    csv_data = pd.read_csv('./cafe-data.csv', encoding="utf-8")
    data_headers = list(csv_data.columns)
    data = csv_data.values.tolist()
    return render_template('cafes.html', cafes=data, headers=data_headers)


if __name__ == '__main__':
    app.run(debug=True)


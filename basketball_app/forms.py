from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, IntegerField, SelectField
from wtforms.validators import (
    InputRequired,
    Optional,
    Length,
    NumberRange,
    ValidationError,
)
from datetime import datetime


class SignupForm(FlaskForm):
    """Form for signing up a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class PlayerForm(FlaskForm):
    """Form for users to search for a NBA player"""

    first_name = StringField("Player First Name", validators=[InputRequired()])
    last_name = StringField("Player Last Name", validators=[InputRequired()])


class AdvancedForm(FlaskForm):
    """Form for advanced search for a NBA player stat"""

    first_name = StringField("Player First Name", validators=[InputRequired()])
    last_name = StringField("Player Last Name", validators=[InputRequired()])
    start_date = DateField("Starting Date (Y-M-D)", validators=[InputRequired()])
    end_date = DateField("End Date (Y-M-D)", validators=[InputRequired()])
    pts = IntegerField(
        "Points (Optional)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Points must be greater or equal to 0!"),
        ],
    )
    reb = IntegerField(
        "Rebounds (Optional)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Rebounds must be greater or equal to 0!"),
        ],
    )
    ast = IntegerField(
        "Assists (Optional)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Assists must be greater or equal to 0!"),
        ],
    )
    stl = IntegerField(
        "Steals (Optional)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Steals must be greater or equal to 0!"),
        ],
    )
    blk = IntegerField(
        "Blocks (Optional)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Blocks must be greater or equal to 0!"),
        ],
    )

    def validate_end_date(form, field):
        try:
            datetime.strptime(str(field.data), "%Y-%m-%d")
            if field.data < form.start_date.data:
                raise ValidationError("End date must not be earlier than start date.")
        except Exception:
            raise ValidationError("Wrong Input Format!")

    def validate_start_date(form, field):
        try:
            datetime.strptime(str(field.data), "%Y-%m-%d")
        except Exception:
            raise ValidationError("Wrong Input Format!")


class TeamsForm(FlaskForm):
    """Form for users to compare two teams"""

    team = SelectField(
        "Team Abbreviation",
        choices=[
            (1, "ALT"),
            (2, "BOS"),
            (3, "BKN"),
            (4, "CHA"),
            (5, "CHI"),
            (6, "CLE"),
            (7, "DAL"),
            (8, "DEN"),
            (9, "DET"),
            (10, "GSW"),
            (11, "HOU"),
            (12, "IND"),
            (13, "LAC"),
            (14, "LAL"),
            (15, "MEM"),
            (16, "MIA"),
            (17, "MIL"),
            (18, "MIN"),
            (19, "NOP"),
            (20, "NYK"),
            (21, "OKC"),
            (22, "ORL"),
            (23, "PHI"),
            (24, "PHX"),
            (25, "POR"),
            (26, "SAC"),
            (27, "SAS"),
            (28, "TOR"),
            (29, "UTA"),
            (30, "WAS"),
        ],
        coerce=int,
    )
    season = IntegerField(
        "Season(Year)",
        validators=[
            InputRequired(),
            NumberRange(
                min=1946, max=2023, message="Year must be between 1946-Current"
            ),
        ],
    )
    postseason = SelectField("Post Season", choices=[("false", "No"), ("true", "Yes")])

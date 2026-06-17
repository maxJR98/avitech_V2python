from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[Optional()])
    price = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Categoría', validators=[Optional()])
    image_url = StringField('URL de imagen', validators=[Optional()])
    is_active = BooleanField('Activo', default=True)

class BranchForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    latitude = FloatField('Latitud', validators=[DataRequired()])
    longitude = FloatField('Longitud', validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    is_active = BooleanField('Activo', default=True)

class DiseaseForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    scientific_name = StringField('Nombre científico', validators=[Optional()])
    description = TextAreaField('Descripción', validators=[Optional()])
    treatment = TextAreaField('Tratamiento', validators=[Optional()])
    prevention = TextAreaField('Prevención', validators=[Optional()])
    keywords = StringField('Palabras clave (separadas por coma)', validators=[Optional()])

class GeneticLineForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[Optional()])

class GrowthTableForm(FlaskForm):
    genetic_line_id = SelectField('Línea genética', coerce=int, validators=[DataRequired()])
    week = IntegerField('Semana', validators=[DataRequired(), NumberRange(min=1)])
    daily_feed_grams = FloatField('Alimento diario (gramos)', validators=[DataRequired(), NumberRange(min=0)])
    daily_water_ml = FloatField('Agua diaria (ml)', validators=[DataRequired(), NumberRange(min=0)])
    weight_kg = FloatField('Peso esperado (kg)', validators=[Optional()])
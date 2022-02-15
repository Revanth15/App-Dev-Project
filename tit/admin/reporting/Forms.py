from wtforms import Form, StringField, SelectField, validators, FieldList, FormField, BooleanField, SelectMultipleField, widgets
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm

from tit.utils import event

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
class CreateReportForm(FlaskForm):
    filename = StringField('Filename', [validators.Length(min=0, max=64, message='filename'), validators.Regexp('([a-zA-Z0-9\s_.])$', message='Please enter valid filename')], default='')
    filetype = SelectField('Filetype', [validators.DataRequired(message='filetype')], choices=[(1, 'Report(.pdf)'), (2, '.xlsx'), (3, '.csv')])
    tags = StringField('Tags', [validators.Length(min=0, max=100, message='tags')], default='')
    images = HiddenField('images', default='')
    charts = MultiCheckboxField('Charts',[validators.Optional()], choices=[(0,'1'), (1,'2'), (2,'3'), (3,'4'), (4,'5'), (5,'6'),(6,'7')], coerce=int)
    

class UpdateReportForm(Form):
    filename = StringField('Filename', [validators.Length(min=0, max=64)], default='')
    filetype = SelectField('Filetype',[validators.Optional()], choices=[(1, 'Report(.pdf)'), (2, '.xlsx'), (3, '.csv')])
    tags = StringField('Tags', [validators.Length(min=0, max=100)], default='')

def createURLMapForm(index, formdata):
    class UpdateURLMap(Form):
        pass

    for name in index:
        setattr(UpdateURLMap, name, StringField(name.upper()))

    form = UpdateURLMap(formdata)
    return form

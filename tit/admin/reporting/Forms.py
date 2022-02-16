from wtforms import Form, StringField, SelectField, validators, FieldList, FormField, BooleanField, SelectMultipleField, widgets
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
class CreateReportForm(FlaskForm):
    filename = StringField('Filename', [validators.Length(min=0, max=64, message='filename')], default='')
    filetype = SelectField('Filetype', [validators.DataRequired(message='filetype')], choices=[(1, 'Report(.pdf)'), (2, '.xlsx'), (3, '.csv')])
    tags = StringField('Tags', [validators.Length(min=0, max=100, message='tags')], default='')
    images = HiddenField('images', default='')
    db = SelectField('Data', choices=[(1, 'Restocks'),(2, 'Notifications'), (3, 'Inventory'), (4, 'Sales'), (5, 'Traffic'), (6, 'Users')])
    charts = MultiCheckboxField('Charts',[validators.Optional()], choices=[(0,'Restocks by SKU'), (1,'Out of Stocks by SKU'), (2,'Inventory Health'), (3,'Revenue over time'), (4,'Sales this month'), (5,'Vistors Today'),(6,'Cart Status')], coerce=int)
    

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

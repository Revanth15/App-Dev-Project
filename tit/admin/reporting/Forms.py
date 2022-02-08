from wtforms import Form, StringField, SelectField, validators, FieldList, FormField
from wtforms.fields.simple import HiddenField

from tit.utils import event

class CreateReportForm(Form):
    filename = StringField('Filename', [validators.Length(min=0, max=64)], default='')
    filetype = SelectField('Filetype', [validators.DataRequired()], choices=[(1, 'Report(.pdf)'), (2, '.xlsx'), (3, '.csv')])
    tags = StringField('Tags', [validators.Length(min=0, max=100)], default='')
    images = HiddenField('images', default='')

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

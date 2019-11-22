from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, Length
from zhsz_api.models import User


class LoginForm(Form):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password',validators=[Length(min=8,max=16)])
    remember = BooleanField('Remember Me')

    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username!')

    def validate_password(self, field):
        if not self.get_user():
            return
        if not self.get_user().check_password(field.data):
            raise ValidationError('Incorrect password!')

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


class RegisterForm(Form):
    username = StringField('Username', validators=[Length(max=64)])
    password = PasswordField('Password',validators=[Length(min=8,max=16)])
    confirm = PasswordField('Confirm Password')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise ValidationError('Username %s already exists!' % field.data)




   
        


        



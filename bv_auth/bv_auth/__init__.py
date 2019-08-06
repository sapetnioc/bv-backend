import binascii
import datetime
import hashlib
import os
from typing import Optional, NoReturn, List

import flask
import jwt

from bv_rest.database import get_cursor

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password


#class User:
    #def __init__(self, login, email, first_name, last_name, institution,
                 #registration_time, email_verification_time,
                 #email_verification_code, activation_time,
                 #deactivation_time):
        #self.login = login
        #self.email_verification_time = email_verification_time
        #if email_verification_code:
            #self.email_verification_code = email_verification_code
        #self.email = email
        #self.first_name = first_name
        #self.last_name = last_name
        #self.institution = institution
        #self.registration_time = registration_time
        #self.activation_time = activation_time
        #self.deactivation_time = deactivation_time
        #self.is_active = (activation_time is not None and
                          #email_verification_time is not None and
                          #deactivation_time is None)
        #self.is_authenticated = True
        #self.is_anonymous = False

    #@staticmethod
    #def _iterate_users(cur, where, where_data):
        #sql = f'SELECT login, email, first_name, last_name, institution, registration_time, email_verification_time, activation_time, deactivation_time FROM cati_portal.identity WHERE {where}'
        #cur.execute(sql, where_data)
        #for row in cur:
            #login, email, first_name, last_name, institution, registration_time, email_verification_time, activation_time, deactivation_time = row
            #if email_verification_time is None:
                #email_verification_code, email = email.split(':', 1)
            #else:
                #email_verification_code = None
            #yield User(login=login,
                       #email=email,
                       #first_name=first_name,
                       #last_name=last_name,
                       #institution=institution,
                       #registration_time=registration_time,
                       #email_verification_time=email_verification_time,
                       #email_verification_code=email_verification_code,
                       #activation_time=activation_time,
                       #deactivation_time=deactivation_time)

    #@staticmethod
    #def get(login, bypass_access_rights=False):
        #if bypass_access_rights:
            #cursor_factory = _get_admin_cursor
        #else:
            #cursor_factory = get_cursor
        #with cursor_factory() as cur:
            #user_generator = User._iterate_users(cur, 'login = %s', [login])
            #try:
                #return next(user_generator)
            #except StopIteration:
                #pass
        #return None

    #@staticmethod
    #def get_from_email_verification_code(email_verification_code):
        #with _get_admin_cursor() as cur:
            #user_generator = User._iterate_users(cur, 'email LIKE %s', [f'{email_verification_code}:%'])
            #try:
                #return next(user_generator)
            #except StopIteration:
                #pass
        #return None

    #@staticmethod
    #def create(login, password, email, first_name=None, last_name=None, institution=None):
        #'''
        #Create a new user in the database
        #'''
        #with _get_admin_cursor() as cur:
            #email_verification_code = str(uuid.uuid4())
            #email = f'{email_verification_code}:{email}'
            #sql = 'INSERT INTO cati_portal.identity(login, password, email, first_name, last_name, institution) VALUES (%s, %s, %s, %s, %s, %s)'
            #cur.execute(sql, [login, password, email, first_name, last_name, institution])
        #return User.get(login, bypass_access_rights=True)

    #def get_id(self):
        #return self.login

    #def check_password(self, password):
        #'''
        #Check the password of a user
        #'''
        #if self.login:
            #with _get_admin_cursor() as cur:
                #sql = 'SELECT password FROM cati_portal.identity WHERE login = %s'
                #cur.execute(sql, [self.login])
                #if cur.rowcount == 1:
                    #hash = cur.fetchone()[0].tobytes()
                    #return check_password(password, hash)
        #return False

    #def has_credential(self, required):
        #'''
        #Verify that the user has a credential
        #'''
        #if self.is_active:
            #l = required.split('.', 1)
            #if len(l) != 2:
                #raise ValueError(f'Invalid credential string "{required}". It must have the form "<project>.<credential>".')
            #project, credential = l
            #with _get_admin_cursor() as cur:
                #sql = 'SELECT COUNT(*) FROM cati_portal.granting WHERE project = %s AND credential = %s AND login = %s'
                #cur.execute(sql, [project, credential, self.login])
                #return (cur.fetchone()[0] == 1)
        #return False

def init_api(api):
    @api.schema
    class NewIdentity:
        login: str
        password: bytes
        email: str
        first_name: Optional[str]
        last_name: Optional[str]
        institution: Optional[str]

    @api.schema
    class Identity(NewIdentity):
        registration_time: Optional[datetime.datetime]
        email_verification_time: Optional[datetime.datetime]
        activation_time: Optional[datetime.datetime]
        deactivation_time: Optional[datetime.datetime]


    @api.path('/public_key')
    def get() -> str:
        '''Return the public key of the authorization server'''
        return open('/bv_auth/id_rsa.pub').read()
    
    @api.path('/api_key')
    @api.may_abort(401)
    def post(login : str, password : str) -> str:
        '''
        Return an API key for this user to use in an authorization header.
        '''
        with get_cursor('bv_services') as cur:
            sql = 'SELECT password FROM identity WHERE login=%s'
            cur.execute(sql, [login])
            if cur.rowcount:
                password_hash = cur.fetchone()[0]
                if verify_password(password_hash, password):
                    now = datetime.datetime.utcnow()
                    obsolete = now + datetime.timedelta(minutes=30)
                    message = {'sub': login,
                            'iss': 'bv_auth',
                            'iat': now,
                            'exp': obsolete,
                            }
                    private_key = open('/bv_auth/id_rsa').read()
                    api_key = jwt.encode(message, private_key, algorithm='RS256').decode('utf8')
                    return api_key
        flask.abort(401, 'Invalid login or password')

    @api.path('/identities')
    @api.require_role('identity_admin')
    def get() -> List[Identity]:
        '''List all identities'''
        with get_cursor('bv_services', as_dict=True) as cur:
            sql = 'SELECT login, email, first_name, last_name, institution, registration_time, email_verification_time, activation_time, deactivation_time FROM identity'
            cur.execute(sql)
            return cur.fetchall()
    
    
    @api.path('/identities')
    @api.require_role('identity_admin')
    def post(identity : NewIdentity) -> Identity:
        '''Create a new identity'''
        with get_cursor('bv_services') as cur:
            time = datetime.datetime.now()
            identity['activation_time'] = time
            identity['email_verification_time'] = time
            identity['registration_time'] = time
            return identity
            sql = 'UPDATE identity SET activation_time = %s, email=%s, email_verification_time = %s WHERE login = %s;'
            cur.execute(sql, [time, user.email, time, user.login])
            sql = 'INSERT INTO cati_portal.granting (login, project, credential) VALUES (%s, %s, %s);'
            cur.executemany(sql, [[user.login, 'cati_portal', 'server_admin'],
                                    [user.login, 'cati_portal', 'user_moderator']])
            flash(f'Administrator {form.login.data} succesfully registered and activated with server and user management rights', 'success')
            user = User.get(user.login, bypass_access_rights=True)
            login_user(user)
            os.remove(hash_file)
            abort(403)
        abort(404)

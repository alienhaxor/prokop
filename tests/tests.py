#!flask/bin/python

import os
import sys
import unittest

sys.path.append('/home/tuhooja/Projects/prokop/')

from app import app, db
from app.main.models import User, Project
from config import basedir


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] \
            = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_check_unique_email(self):
        u = User(name='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        result = User.check_unique_email('john@example.com')
        assert result is not False
        result = User.check_unique_email('john2@example.com')
        assert result is False
        result = User.check_unique_email('john@example.com')
        assert result is True
        # u = User(name=result, email='susan@example.com')
        # db.session.add(u)
        # db.session.commit()
        # result2 = User.check_unique_email('john')
        # assert result2 != 'john'
        # assert result2 != result

    #unique project name
    def test_check_unique_proj_name(self):
        p = Project(name='asd')
        db.session.add(p)
        db.session.commit()
        result = Project.check_unique_proj_name('asd')
        assert result is not False
        result = Project.check_unique_proj_name('asd2')
        assert result is False

    def test_check_unique_proj_url(self):
        p = Project(url='asd')
        db.session.add(p)
        db.session.commit()
        result = Project.check_unique_proj_url('asd')
        assert result is not False
        result = Project.check_unique_proj_url('asd2')
        assert result is False


if __name__ == '__main__':
    unittest.main()

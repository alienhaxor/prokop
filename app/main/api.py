from flask.ext.restful import Resource, reqparse, fields, marshal
import os, json

from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for, jsonify, abort, make_response

from app import app, db, bcrypt, api
from app.main.models import User, Project, Project_image


class ProjectListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No task name provided',
                                   location='json')

        self.reqparse.add_argument('info', type=str, default="",
                                   location='json')

        self.reqparse.add_argument('fileField', type=str, default="",
                                   location='json')

        super(ProjectListAPI, self).__init__()

    def get(self):
        return jsonify(Projects=[i.serialize for i in Project.query.all()])

    def post(self):
        args = self.reqparse.parse_args()
        project = Project(name=args['name'], info=args['info'])
        db.session.add(project)
        fileData = args['fileField']

        if fileData is not 'False':
            files = json.loads(fileData)

            for file in files['items']:
                img = Project_image(url=file['file'])

                if file['cover'] == 1:
                    img.cover = True
                project.images.append(img)
        db.session.commit()
        #return jsonify(Project=[project.serialize()]), 201
        return {'result': True}


class ProjectAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('info', type=str, location='json')
        super(ProjectAPI, self).__init__()

    def get(self, id):
        project = Project.query.get(int(id))
        if not project:
            abort(404)
        return jsonify(Projects=[project.serialize])

    def put(self, id):
        project = Project.query.get(int(id))
        if not project:
            abort(404)
        args = self.reqparse.parse_args()
        if args.name is not None:
            project.name = args.name
        if args.info is not None:
            project.info = args.info
        return jsonify(Project=[project.serialize()])

    def delete(self, id):
        project = Project.query.get(int(id))
        if not project:
            abort(404)
        db.session.delete(project)
        db.session.commit()
        return {'result': True}

api.add_resource(ProjectListAPI,
                 '/api/v1.0/projects')

api.add_resource(ProjectAPI,
                 '/api/v1.0/projects/<int:id>')


class ProjectPersonListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='No task name provided',
                                   location='json')

        self.reqparse.add_argument('role', type=str, default="",
                                   location='json')

        super(ProjectPersonListAPI, self).__init__()

    def get(self):
        return jsonify(Projects=[i.serialize for i in User.query.all()])

    def post(self):
        args = self.reqparse.parse_args()
        user = User(name=args['name'], info=args['info'])
        db.session.add(user)
        return {'result': True}


class ProjectPersonAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, default="")
        self.reqparse.add_argument('role', type=str, default="1")
        super(ProjectPersonAPI, self).__init__()

    def get(self, id, person_id):
        args = self.reqparse.parse_args()
        #role = request.args['role']
        person_id = person_id
        role = args['role']
        return {'person_id': person_id, 'role': role}

    def delete(self, id):
        user = User.query.get(int(id))
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return {'result': False}


api.add_resource(ProjectPersonListAPI,
                 '/api/v1.0/projects/<int:id>/persons')

api.add_resource(ProjectPersonAPI,
                 '/api/v1.0/projects/<int:id>/persons/<int:person_id>')

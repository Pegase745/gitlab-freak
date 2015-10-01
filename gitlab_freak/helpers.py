from __future__ import absolute_import, unicode_literals
from distutils.version import LooseVersion
from sqlalchemy.sql.expression import ClauseElement
from flask import Flask
import json
import requests


from gitlab_freak.models import db, ProjectDependency

import gitlab

app = Flask(__name__)
app.config.from_envvar('GITLAB_FREAK_SETTINGS')

git = gitlab.Gitlab(app.config['GITLAB_ENDPOINT'], app.config['GITLAB_TOKEN'])


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict(
            (k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def nodeLatestVersion(dependency, project_id):
    r = requests.get('%s%s/latest' % (app.config['NPM_REGISTRY'], dependency))
    latestVersion = r.json().get('version')

    try:
        dep = ProjectDependency.by_project(project_id, dependency)
        dep.latest_version = latestVersion
        if LooseVersion(dep.actual_version) < LooseVersion(latestVersion):
            dep.status = 'ko'
        else:
            dep.status = 'ok'
        db.session.commit()
    except Exception, e:
        app.logger.error(e)
        db.session.rollback()


def nodeDepsFetcher(project_id):
    # Get dependencies from package.json
    project = git.getproject(project_id)

    depFileEncoded = git.getfile(project_id, 'package.json',
                                 project['default_branch'])

    # Decode from base64
    deps = json.loads(depFileEncoded.get('content').decode('base64'))

    mainDeps = deps.get('dependencies')
    devDeps = deps.get('devDependencies')

    # Insert in project_dependency
    # TODO create single function for that
    for mDep, mVersion in list(mainDeps.items()):
        mdep, created = get_or_create(db.session, ProjectDependency,
                                      project_id=project_id, name=mDep,
                                      actual_version=mVersion)

        if not created:
            app.logger.info('[%s] Dep %s already exist' % (project_id, mDep))

        db.session.commit()
        nodeLatestVersion(mDep, project_id)

    for devDep, devVersion in list(devDeps.items()):
        ddep, created = get_or_create(db.session, ProjectDependency,
                                      project_id=project_id, name=devDep,
                                      actual_version=devVersion, dev=True)

        if not created:
            app.logger.info('[%s] Dev dep %s already exist' %
                            (project_id, devDep))

        db.session.commit()
        nodeLatestVersion(devDep, project_id)
    return True

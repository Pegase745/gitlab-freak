#!/usr/bin/env python
from gitlab_freak import app

app.run('0.0.0.0', port=5678, debug=True)

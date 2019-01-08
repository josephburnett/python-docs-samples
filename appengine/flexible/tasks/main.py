# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""App Engine app to serve as an endpoint for App Engine queue samples."""

# [START cloud_tasks_appengine_quickstart]
from __future__ import print_function
from flask import Flask, request

import argparse
import datetime

app = Flask(__name__)


@app.route('/example_task_handler', methods=['POST'])
def example_task_handler():
    """Log the request payload."""
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: {}'.format(payload))
    return 'Printed task payload: {}'.format(payload)
# [END cloud_tasks_appengine_quickstart]


@app.route('/')
def hello():
    """Basic index to verify app is serving."""
    return 'Hello World 5!'

@app.route('/make_me_a_task')
def make_me_a_task():
    create_task()
    return 'did i...do it?'

def create_task():
    # [START cloud_tasks_appengine_create_task]
    """Create a task for a given queue with an arbitrary payload."""

    from google.cloud import tasks_v2beta3
    from google.protobuf import timestamp_pb2

    # Create a client.
    client = tasks_v2beta3.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'joe-does-flex'
    queue = 'my-appengine-queue'
    location = 'us-central1'
    payload = 'hello'

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'relative_uri': '/example_task_handler'
            }
    }
    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task['app_engine_http_request']['body'] = converted_payload

    # if in_seconds is not None:
    #     # Convert "seconds from now" into an rfc3339 datetime string.
    #     d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

    #     # Create Timestamp protobuf.
    #     timestamp = timestamp_pb2.Timestamp()
    #     timestamp.FromDatetime(d)

    #     # Add the timestamp to the tasks.
    #     task['schedule_time'] = timestamp

    # Use the client to build and send the task.
    response = client.create_task(parent, task)

    print('Created task {}'.format(response.name))
    return response


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

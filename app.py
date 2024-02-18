import os
from flask import Flask, render_template, Response, send_from_directory
from .kafka_utils import get_kafka_consumer
from dotenv import load_dotenv
load_dotenv(".env")


app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: Rendered HTML content.
    """
    return render_template('index.html')


@app.route('/static/airplane-icon.svg')
def get_airplane_icon() -> bytes:
    """
    Get the airplane icon from the 'static' directory.

    Returns:
        bytes: Binary content of the airplane icon SVG file.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'airplane-icon.svg')


# Consumer API
@app.route('/topic/<topicname>')
def get_messages(topicname):
    def events():
        consumer = get_kafka_consumer(topicname)
        try:
            for message in consumer:
                yield 'data:{0}\n\n'.format(message.value)
        finally:
            consumer.close()

    return Response(events(), content_type="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

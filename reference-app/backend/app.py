from asyncio.log import logger
from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)


@app.route("/")
@metrics.do_not_track()
def homepage():
    return "Hello World"


@app.route("/api")
@metrics.do_not_track()
def my_api():
    answer = "API response body"
    return jsonify(repsonse=answer)


@app.route("/star")
@metrics.summary('add_star_requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
def add_star():
    output = {}
    with tracer.start_span("add_star") as span:
        span.log_kv({"event": "add star", "request": request})
        span.set_tag("request", request)
        star = mongo.db.stars
        star_id = star.insert({"name": "a", "distance": 10})
        new_star = star.find_one({"_id": star_id})
        span.set_tag("result", new_star)
        span.set_tag("http.status_code", 405)
        output = {"name": new_star["name"], "distance": new_star["distance"]}
        logger.info(f"final output after adding start is {new_star}")

    return jsonify({"result": output})

@app.route("/success")
@metrics.summary('success_requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
def success():
    with tracer.start_span("request_status") as span:
        span.set_tag("status_code", 200)
    return "Success", 200

@app.route("/error")
@metrics.summary('error_requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
def error():
    with tracer.start_span("request_status") as span:
        span.set_tag("status_code", 500)
    return "Error", 500

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == "__main__":
    app.run()
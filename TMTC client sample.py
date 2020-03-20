Sending a simple event telemetry item

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.track_event('Test event')
tc.flush()
Sending an event telemetry item with custom properties and measurements

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.track_event('Test event', { 'foo': 'bar' }, { 'baz': 42 })
tc.flush()
Sending a trace telemetry item with custom properties

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.track_trace('Test trace', { 'foo': 'bar' })
tc.flush()
Sending a metric telemetry item

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.track_metric('My Metric', 42)
tc.flush()
Sending an exception telemetry item with custom properties and measurements

import sys
from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
try:
    raise Exception('blah')
except:
    tc.track_exception()

try:
    raise Exception("blah")
except:
    tc.track_exception(*sys.exc_info(), properties={ 'foo': 'bar' }, measurements={ 'x': 42 })
tc.flush()
Configuring context for a telemetry client instance

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.context.application.ver = '1.2.3'
tc.context.device.id = 'My current device'
tc.context.device.oem_name = 'Asus'
tc.context.device.model = 'X31A'
tc.context.device.type = "Other"
tc.context.user.id = 'santa@northpole.net'
tc.context.properties['my_property'] = 'my_value'
tc.track_trace('My trace with context')
tc.flush()
Establishing correlation between telemetry objects

context field called operation_id can be set to associate telemetry items. Since operation_id is being set as a property of telemetry client, the client shouldn't be reused in parallel threads as it might lead to concurrency issues.

tc = TelemetryClient(instrumentation_key=instrumentation_key)
tc.context.operation.id = <operation_id>
tc.track_trace('Test trace')
tc.flush()
Configuring channel related properties

from applicationinsights import TelemetryClient
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
# flush telemetry every 30 seconds (assuming we don't hit max_queue_item_count first)
tc.channel.sender.send_interval_in_milliseconds = 30 * 1000
# flush telemetry if we have 10 or more telemetry items in our queue
tc.channel.queue.max_queue_length = 10
Configuring TelemetryProcessor

from applicationinsights import TelemetryClient
def process(data, context):
   data.properties["NEW_PROP"] = "MYPROP"  # Add property
   context.user.id = "MYID"   # Change ID
   return True # Not filtered
tc = TelemetryClient('<YOUR INSTRUMENTATION KEY GOES HERE>')
tc.add_telemetry_processor(process)
Basic logging configuration (first option)

import logging
from applicationinsights.logging import enable

# set up logging
enable('<YOUR INSTRUMENTATION KEY GOES HERE>')

# log something (this will be sent to the Application Insights service as a trace)
logging.info('This is a message')

# logging shutdown will cause a flush of all un-sent telemetry items
logging.shutdown()
Basic logging configuration (second option)

import logging
from applicationinsights.logging import LoggingHandler

# set up logging
handler = LoggingHandler('<YOUR INSTRUMENTATION KEY GOES HERE>')
logging.basicConfig(handlers=[ handler ], format='%(levelname)s: %(message)s', level=logging.DEBUG)

# log something (this will be sent to the Application Insights service as a trace)
logging.debug('This is a message')

try:
    raise Exception('Some exception')
except:
    # this will send an exception to the Application Insights service
    logging.exception('Code went boom!')

# logging shutdown will cause a flush of all un-sent telemetry items
# alternatively flush manually via handler.flush()
logging.shutdown()
Advanced logging configuration

import logging
from applicationinsights import channel
from applicationinsights.logging import LoggingHandler

# set up channel with context
telemetry_channel = channel.TelemetryChannel()
telemetry_channel.context.application.ver = '1.2.3'
telemetry_channel.context.properties['my_property'] = 'my_value'

# set up logging
handler = LoggingHandler('<YOUR INSTRUMENTATION KEY GOES HERE>', telemetry_channel=telemetry_channel)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
my_logger = logging.getLogger('simple_logger')
my_logger.setLevel(logging.DEBUG)
my_logger.addHandler(handler)

# log something (this will be sent to the Application Insights service as a trace)
my_logger.debug('This is a message')

# logging shutdown will cause a flush of all un-sent telemetry items
# alternatively flush manually via handler.flush()
logging.shutdown()
Logging unhandled exceptions

from applicationinsights.exceptions import enable

# set up exception capture
enable('<YOUR INSTRUMENTATION KEY GOES HERE>')

# raise an exception (this will be sent to the Application Insights service as an exception telemetry object)
raise Exception('Boom!')

# exceptions will cause a flush of all un-sent telemetry items
Logging unhandled exceptions with context

from applicationinsights import channel
from applicationinsights.exceptions import enable

# set up channel with context
telemetry_channel = channel.TelemetryChannel()
telemetry_channel.context.application.ver = '1.2.3'
telemetry_channel.context.properties['my_property'] = 'my_value'

# set up exception capture
enable('<YOUR INSTRUMENTATION KEY GOES HERE>', telemetry_channel=telemetry_channel)

# raise an exception (this will be sent to the Application Insights service as an exception telemetry object)
raise Exception('Boom!')

# exceptions will cause a flush of all un-sent telemetry items
Integrating with Flask

from flask import Flask
from applicationinsights.flask.ext import AppInsights

# instantiate the Flask application
app = Flask(__name__)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '<YOUR INSTRUMENTATION KEY GOES HERE>'

# log requests, traces and exceptions to the Application Insights service
appinsights = AppInsights(app)

# define a simple route
@app.route('/')
def hello_world():
    # the following message will be sent to the Flask log as well as Application Insights
    app.logger.info('Hello World route was called')

    return 'Hello World!'

# run the application
if __name__ == '__main__':
    app.run()

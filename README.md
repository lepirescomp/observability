Containerize four python applications, backend, frontend and two small 
ones to test purposes. Frontend uses multithread. Orchestrate the 
containers with kubernetes and expose it through ports to provide the data 
to Prometheus and read them in Grafana and Jaeger. Grafana provides a good 
visibility of the elements of the system health through dashboards and 
Jaeger shows the tracing of the most important endpoints. 

## Verifing the pods of the monitoring, observabiity and default namespaces installation

![Screenshot](/img/monitoring_app.png)

![Screenshot](/img/monitoring_instalation.png)

## Setup of the Jaeger and Prometheus source

![Screenshot](/img/grafana_login.png)
![Screenshot](/img/frontend_localhost8080.png)


## Basic Dashboard

![Screenshot](/img/data_source.png)


## Defining SLO/SLI

A Service-Level Indicator (SLI) is a specific metric used to measure the performance of a service.
At the end, it is a actual mesuarement. For example, the application will have an uptime of 99.9% during the next year. When you think of SLIs, think in terms of ratios like this—a ratio of X / Y, where X is usually a measurement and Y is usually an amount of time.
 

## Creating SLI metrics.

SLO:  uptime - SLI: time a service is active. 
SLO:  latency - SLI: response time of requests
SLO:  Failure rate - SLI: amount of failures in a unit of time.
SLO:  Network capacity - SLI: average bandwidth in a specifi period of time.
SLO:  Resource capacity - SLI: amount of CPU and RAM usage.


##  Dashboard to measure our SLIs

![Screenshot](/img/dashboard1frontend.png)
![Screenshot](/img/dashboard2frontend.png)


## Tracing our Flask App

 ![Screenshot](/img/jaeger_backend.png)
 ![Screenshot](/img/jaeger_backend_dashboard.png)
 ![Screenshot](/img/spam_success_endpoint.png)

## Jaeger in Dashboards



![Screenshot](/img/jaeger_grafana_httpstatuscode_200.png)

## Tracing an endpoint which retuns an error status

![Screenshot](/img/tracebackspanjaegererrordatabase.png)


## Creating SLIs and SLOs

SLOs:

99.95% of availability/month.

Maximum latency of application should be less them 300 ms on average per month.

Memory usage should not go more than 500Mb per month.

CPU resource request should be above the treshold of 70% per month.

SLIs:

20x or 30x responses of the service for the month is 99.95%.

Average latency of requests is 1037ms for the month.

Average memory usage by the application is 300Mib for the month.

Average CPU usage by the services is 45.00% for the month

## Building KPIs plan
KPI/Plan as follows:

1. 20x or 30x responses of the service for the month is 99.95%
    - uptime per month, determines the usability of service with this KPI.
    - KPI indicates the availability of the services.

2. Average latency of requests is 300ms for the month.
    - latency of the application can be indicated from this KPI.

3. Average CPU usage by the services is 40.90% for the month
    - cpu usage - CPU used by the pod for a given service can be indicated by this KPI.
    - threshold of cpu usage is a good indicator for this KPI 

4. Average memory usage by the application is 247Mib for the month.
    - memory usage - memmory usage used by the pod for a given service can be indicated by this KPI.
    - threshold of memory usage is a good indicator for this KPI 



## Dashboard for the KPIs monitoring

![Screenshot](/img/finaldhasboard.png)



"Uptime" panel - Shows the successful responses of the service.

"Average Response Time" panel - It shows the average response time of the service per request.

"CPU Usage" panel - CPU usage of each pod.

"Memory Usage" panel - The usage of memory.

Adding to them, an important metric to monitor:

"Error rate" panel - The rate of errors 5xx and 4xx of the application.




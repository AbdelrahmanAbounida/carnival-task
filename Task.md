# Prerequisites

## Optimization service

We currently have an optimization service that creates optimization results based on various criteria, such as a route,
weather, power consumption etc. The result of such an optimization for a route from the port "OMSTQ" to the port "AEJEA"
can be seen in the file "optimization_OMSTQ_AEJEA.csv". As of now, this file is only written by the optimization
service on an EFS storage it uses.

## Route service

In addition, we also have a route service. This service provides a route geometry for a given departure and arrival
port un_locode. The file "route_OMSTQ_AEJEA.json" contains an example for a REST API response that contains
the geometry for the route from "OMSTQ" to "AEJEA". The response is in a geojson structure. The endpoint looks like
this:
`GET /route?departure_port_un_locode=<un_locode>&arrival_port_un_locode=<un_locode>`

The service also has a second endpoint, which returns information on which fuel is allowed to be used for which region
within certain route. This response refers to regions as geodesic distances on the route. So for instance, if an area
starts at 0 and ends at 100, this means that the allowed fuel of this region can be used from the nautical mile 0 until
the nautical mile 100 on the route. This endpoint also operates with port un_locodes and a response for the route from
"OMSTQ" to "AEJEA" can be seen in the file "allowed_fuels_OMSTQ_AEJEA.json". The endpoint looks like this:
`GET /allowed-fuels?departure_port_un_locode=<un_locode>&arrival_port_un_locode=<un_locode>`

# Task

We want to build a new compliance service from scratch. This service should check if an optimization result follows the
fuel allowances for the route that the optimization was performed for. We have the following requirements:

- Utilize the output from the optimization service. Note that it is currently only stored on a storage within the
  optimization service, so you have to decide how to provide it from that service to the compliance service. You do not
  have to implement any changes that have to be made on the optimization service side, but you have to provide
  everything necessary on the consumer side (i.e. the compliance service).
- You should utilize the example response files and endpoint definitions that are provided for the route service. You
  can use those files to mock the route service or its responses in whichever way you see fit.
- The compliance service should provide an endpoint that checks whether an optimization is compliant. It should provide
  an appropriate response containing information on which parts of the optimization might not be compliant and why. For
  now, input parameters for this endpoint could be the departure and arrival port un_locodes.
- As the service might have some request loads in the future (e.g. 60 requests/minute), consider scalability of the
  service.
- Consider that the optimization result only contains a limited amount of points and does not reflect the original
  geometry of the route.
- Use a python framework of your choosing, preferably FastAPI.

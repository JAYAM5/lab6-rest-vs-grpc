
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	| 3.028961711999955 | 4.227123121000005 | 306.57431481000003 |
|   gRPC add	| 1.190310259999933	| 1.4081891700000142 | 148.53547987999946	|
|   REST rawimg	| 5.973129602000029	| 10.663697344000013 | 1220.0867898400008 |
|   gRPC rawimg	| 14.53166834800004 | 15.276658653999903 | 175.851408420001	|
|   REST dotproduct	| 4.494497476999982 | 5.358804573999976 | 307.91538556999967 |
|   gRPC dotproduct	| 1.238315232000332 | 1.6136093509999228 | 148.85424452000052 |
|   REST jsonimg	| 41.67258258099997 | 47.12350685000001 | 1378.5730574599995 |
|   gRPC jsonimg	| 38.9891053020001 | 41.144347717999835	| 204.64072294999823 |
|   PING        | 0.044 | 0.396 | 148.667 |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

In nearly all instances, gRPC exhibited lower average operation time. The only exception is for raw image transmission, where gRPC was slower for both local and same-zone tests; however, while REST massively spiked for a different region, gRPC also increased but remained consistent with other gRPC increases across different regions. Ping also increased from local and same-zone to different region. The benefits of gRPC (namely, leveraging a single TCP connection vs reestablishing one for each transaction) are evident when comparing the two methods side by side, in particular for transactions occurring across different regions. In terms of latency, ping increases by 148 ms from same zone to different region, which is evident in the approximate increases for gRPC tests. Meanwhile, the REST increases from local/same-zone to different region outstrip corresponding ping increases, in particular for jsonimg and rawimg. The highest latency exhibited came from REST jsonimg and rawimg - perhaps this can be expected due to the size of the transmission and for the jsonimg results in particular, overhead with decoding the received messages.

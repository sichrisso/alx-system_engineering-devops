## 0x19-postmortem
![BUG](https://i.pinimg.com/564x/74/68/56/74685691970bbb2e0c1b2c7176fb5d05.jpg)


## Issue summary 

16/10/21 From 8:34 PM to 9:16 PM EAT,  
E-Merkato, our major e-commerce brand in Bytech went down for 42 minutes. The site went down after sudden traffic spike caused by a marketing campaign. The outage was caused by configuration error in cluster resource management which prevented more service instances from starting even though hardware resources were available. 

## Timeline
The special offer was to start at 8:30 PM, and a direct link to its item page had been published before. 

| Time | Description |
| ----- | ----------- |
| 08:15 | We manually scaled out the listing service to be prepared for increased incoming traffic  |
| 08:21 | Traffic of the major services was already 50% higher than the day before at the same time of day   |
| 08:26 | Further traffic increase causing response times of major services to rise, forcing us to scale out these services |
| 08:29 | Almost all resources in the part of the cluster provisioned for these services had beem reserved even though only a fraction of the cluster’s capacity was actually used  |
|       | As we later found out, due to a misconfiguration, some services reserved much more resources that they actually needed. This lead to a paradoxical situation in which there were plenty of resources available int the cluster but since they were reserved, they couldn’t be assigned to any other services  |
| 08:29 | Traffic peaked at 200% - 300% of the traffic from the previous day, due to excessive resource reservation, in some parts of the cluster we couldn’t use available CPUs and RAM for starting new services  |
|       | Meanwhile, the frontend service, was starting to fail, causing a decrease in traffic to backend services.  |
| 08:30 | The price of the special offer was updated & the first sales took place  |
| 08:34 | Our monitoring tool DATADOG detected the incident |
|       | DATADOG alerts the on-call system (paperduty)  |
| 08:35 | The on-call team was alerted |
| 08:41 | The on-call person acknowledged the alert   |
| 08:50 | The cluster started killing off unresponsive instances. While automated and manual scaling efforts continued  |
| 08:59 | On-call team started adding more resources to the cluster. At the same time, we started shutting down some non-critical services in order to free CPU and memory |
| 09:16 | The situation was fully under control And E-Merkato became responsive again |


## Root cause and resolution 
The direct cause was a special offer in which 50 Samsung galaxy s20 ultra phones whose regular price is around 50,000 birr (1,000$), were offered a 45% discount at a price of 27,500 birr (550$). This attracted more traffic than anticipated and at the same time triggered a configuration error in the way services are scaled out. This caused the site to go down despite there being plenty of CPUs, RAM, and Network capacity available in our data centers.

To solve the problem we made it possible to finish the transaction afterwards to buyers who managed to buy the phone at the low price but whose transactions were aborted as the system went down. 

We prepare internal postmortems after any serious issue in order to analyze the causes and learn from our mistakes. This is prepared by our team leader Yunus Kidem that took part in dealing with the outage. 
What is going on inside a service which experiences traffic higher than it can handle with available resources? As response times increase, the autoscaler tries to scale up the service. On the other hand, instances whose health endpoint can’t respond within a specified timeout, are automatically shut down. During the outage, autoscaler did not respond quickly enough to rising traffic and we had to scale up manually. There were also some bad interactions between the autoscaler scaling services up and the cluster watchdog killing off unresponsive instances.

![code confesses](https://pics.me.me/idontuse-debuggers-istare-down-until-the-code-confesses-memes-thats-10674287.png)

## Corrective and preventative measures
The observation that new Opbox instances had issues while starting under high load. Newly started instances very quickly reached “unresponsive” status and were automatically killed. We will try out several ideas which should make the service start up faster even if it gets hit with lots of requests right away.

Finally, by introducing smart caches, we should be able to eliminate the need for many requests altogether. Due to personalisation, item pages are normally not cached and neither is the data returned by backend services used for rendering those pages. However, we plan to introduce a mechanism which will be able to tell backend services to generate simplified, cacheable responses under special conditions. This will allow us to decrease load under heavy traffic.

Apart from the need of introducing the improvements mentioned above, we learned a few other interesting things.
First off, we certainly learned that traffic drawn in by an attractive offer can outgrow our expectations. We should have been ready for more than we were, both in terms of using cluster capacity effectively and in terms of general readiness to handle unexpected situations caused by a sudden surge in traffic. Apart from technical insights, we also learned some lessons on the business side of things, related to dealing with attractive offers and organizing promotions, for example that publishing a direct link to the special offer ahead of time was a rather bad idea.

Interestingly enough, the traffic which brought us down, was in large part bots rather than human users. Apparently, some people were so eager to buy the phone cheaply that they used automated bots in order to increase their chances of being in the lucky hundred. Some even shared their custom solutions online. Since we want to create a level playing field for all users, we plan to make it harder for bots to participate in this kind of offers.
Even though it may have looked as if the site had gone down due to an exhaustion of resources such as processing power or memory, actually plenty of these resources were available. However, an invalid approach to reserving resources made it impossible at one point to use them for starting new instances of the services which we needed to scale out.

I think that despite the outage taking place, the way we handled it validated our approach to architecture. Thanks to the cloud, we were able to scale out all critical services as long as the resource limits allowed us to. Using microservices, we were able to scale different parts of the system differently which made it possible to use the available cluster more effectively. Loose coupling and separation of concerns between the services allowed us to safely shut down those parts of the system which were not critical in order to make room for more instances of the critical services.

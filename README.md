# COMP5622_IoT_Guard_Experiment

This repository aims for faciliate experiments related to IoT security. We would like to verify the effectiveness of the proposed solution. 

## Proposed solution 
----------------
![](https://github.com/KuoTzu-yang/COMP5622_IoT_Guard_Experiment/blob/master/pictures/approach_diagram.jpg)

The intuition is that a desirable solution should satisfy both trust-free and non-consumption of much computational capability on IoT devices properties. Also, it will be beneficial to leverage the aggregated traffic information through the gateway, especially for attacks like IoT-DDoS.  

## Basic principle and explanations
----------------
a. This model leverages aggregated traffic information (ATI for short) via the gateway. ATI represents the overall traffic situation among the local topology, which is extremely helpful against attacks like IoT-DDoS. 

b. Among IoT devices, some of IoT devices like laptops and phones possess more computational capability than the others, let’s call them guards. By leveraging the computational capability of guards, the local IoT system no longer needs to communicate with a remote third-party.

c. With sufficient computational capability, guards can perform security detection algorithm for IoT-DDoS and other cyber attacks on IoT devices, either for individual IoT transmission packet or the entire local IoT system. If guard perceives any abnormal situation, it will respond with a corresponding instruction to the gateway, in which instruction will be further separated into actions for each IoT devices. Otherwise, guards will simply wait for another ATI.

d. The number of guards can vary. Essentially, one guard is enough. Adding more guards can improve the overall performance of the local IoT system. 

e. For most of IoT devices expect guards, there is no modification imposed on them. These IoT devices are not aware of the added security protection.  

f. Different local IoT systems do not use the same cloud center for executing the security algorithm. For each local IoT system, they select local IoT devices as guards and leverage the computational capability of guards. Therefore, this solution is not restricted to the scalability issue. 
   
Configuration
----------------
  Python: 3.6.7  
  NumPy: 1.14.2 

References
----------------
  Uzair Javaid, Ang Kiang Siang, Muhammad Naveed Aman, Biplab Sikdar <br/>
  Mitigating IoT device based DDoS Attacks using Blockchain, Cryblock, MobiSys ‘18, Munich, Germany <br/>
  https://www.ece.nus.edu.sg/stfpage/bsikdar/papers/cryblock_18.pdf <br/>
  
  Bhardwaj, Ketan & Chung M., Joaquin F. & Gavrilovska, Ada. (2018) <br/>
  Towards IoT DDoS Prevention Using Edge Computing <br/>
  https://www.usenix.org/system/files/conference/hotedge18/hotedge18-papers-bhardwaj.pdf <br/>

  salarn/OPENRP GitHub repository, Wifi Direct API <br/>
  https://github.com/salarn/OPENRP <br/>

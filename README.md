# HKUST COMP5622 Project

This repository aims for faciliate experiments related to IoT security, which verifies the effectiveness of the proposed solution. 

## Proposed solution 
----------------
![](https://github.com/KuoTzu-yang/COMP5622_IoT_Guard_Experiment/blob/master/pictures/approach_diagram.jpg)

The intuition is that a desirable solution should satisfy both trust-free and non-consumption of much computational capability on IoT devices properties. Also, it will be beneficial to leverage the aggregated traffic information through the gateway, especially for attacks like IoT-DDoS.  

## Basic principle and explanations
----------------
* This model leverages aggregated traffic information (ATI for short) via the gateway. ATI represents the overall traffic situation among the local topology, which is extremely helpful against attacks like IoT-DDoS. 

* Among IoT devices, some of IoT devices like laptops and phones possess more computational capability than the others, let’s call them guards. By leveraging the computational capability of guards, the local IoT system no longer needs to communicate with a remote third-party.

* With sufficient computational capability, guards can perform security detection algorithm for IoT-DDoS and other cyber attacks on IoT devices, either for individual IoT transmission packet or the entire local IoT system. If guard perceives any abnormal situation, it will respond with a corresponding instruction to the gateway, in which instruction will be further separated into actions for each IoT devices. Otherwise, guards will simply wait for another ATI.

* The number of guards can vary. Essentially, one guard is enough. Adding more guards can improve the overall performance of the local IoT system. 

* For most of IoT devices expect guards, there is no modification imposed on them. These IoT devices are not aware of the added security protection.  

* Different local IoT systems do not use the same cloud center for executing the security algorithm. For each local IoT system, they select local IoT devices as guards and leverage the computational capability of guards. Therefore, this solution is not restricted to the scalability issue. 
   
Main Dependency 
----------------
  Python: 3.6.7  
  NumPy: 1.14.2 

References
----------------
   [1] U. Javaid, A. K. Siang, M. N. Aman, and B. Sikdar, ‘‘Mitigating loT
   device based DDoS attacks using blockchain,’’ in Proc. 1st Workshop
   Cryptocurrencies Blockchains Distrib. Syst., 2018, pp. 71–76 <br/>
   [2] K. Bhardwaj, J. C. Miranda, and A. Gavrilovska,
   “Towards IoT-DDoS prevention using edge
   computing,” in Proc. USENIX Workshop Hot Topics
   Edge Comput. (HotEdge 18), 2018.<br/>
  
GitHub Repo. 
----------------
   OPENRP https://github.com/salarn/OPENRP 

# MySample

1. ParkingManagement
 - 熟悉理解栈和队列的逻辑结构和存储结构，设计实现停车场管理的模拟系统，其主要内容如下：
 设停车场是一个可以停放n辆汽车的狭长通道，且只有一个大门可供汽车进出，其模型如下图所示。
 汽车在停车场内按车辆到达时间的先后顺序，依次由北向南排列（大门在最南端，最先到达的第一辆汽车停放在车场的最北端）。
 若车场内已停满n辆车，那么后来的汽车能在门外的便道上等候，一旦有车开走，则排在便道上的第一辆车即可开入。
 当停车场内某辆汽车要离开时，在它之后进入的车辆必须先退出停车场按顺序开入临时停放道为其让路，待其开出大门外后，再按原次序进入车场。
 每辆停放在停车场的汽车在它离开停车场时必须按其停留的时间长短缴纳费用（从进入停车场开始计费）。
 
 ![Image text](https://img-blog.csdnimg.cn/20190111154632205.png)

 - 车库和临时停放车道都是栈
 便道是队列
 计费使用时间函数读取以秒为单位的系统时间乘上每秒的费用
 停车时间以数组形式存储在车库栈的结构体中，以车位（栈序号）存储
 每当有新车进入车库，读取系统时间记录于停车时间数组中
 每当有车辆驶出，根据现在时间结算费用；并依次移动栈的车辆序号和时间数组
 题目要求的“必须先退出停车场按顺序开入临时停放道为其让路，待其开出大门外后，再按原次序进入车场“在函数DriveOut中实现；无输出结果；

2. MyChat
 - Python
 - GUI MultiThreading Socket
 
3. CrawlerForZhengfang
 - Python
 - Crawler

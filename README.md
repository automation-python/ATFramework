# ATFramework


----------
# 环境依赖

    pip install PyYAMl

----------
# 程序入口

    run runTest.py
    
----------
# 脚本路径配置
    config = {
        "casePath":"login,pay"
    }

----------
# 目录结构

    ├── Readme.md                   // help
    ├── runTest                     // 程序入口
    ├── ATFramework                 // 接口框架
    │   ├── commoe                  
    │   ├── runner                 
    │   ├── utils
    │   ├── xmlrunner
    |   ├── project
    ├── AW                          // 接口具体实现
    ├── Report                      // 结果报告
    ├── Scripts                     // 待定
    ├── yaml                        // 脚本文件
    
----------
# 框架思路
脚本分为data（数据文件）和logic（逻辑文件），用户需自己实现接口请求部分，通过casePath配置可实现单个接口或者整个流程所有接口的调用

# 待完善功能
 1. 压力测试

# 已支持功能
1. 脚本路径支持“”（全量执行）、data、logic、文件夹路径执行
2. 支持logic文件多对一，casePath为logic文件路径时，可解析所有对应data文件
3. 结果报告展示

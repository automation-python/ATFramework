# ATFramework
一个慢慢完善的接口自动化框架

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
    │   ├── project
    ├── AW                          // 接口具体实现
    ├── Report                      // 结果报告
    ├── Scripts                     // 待定
    ├── yaml                        // 脚本文件
    
----------
# 框架思路
暂无

# 待完善功能
 1. 压力测试
 2. 结果报告展示截图（待完善）、结果报告执行情况图表展示（待完善）

# 已更新功能
优化脚本解析
1. 脚本路径支持“”（全量执行）、data、logic、文件夹路径执行，可自动去重
2. 支持logic文件多对一，casePath为logic文件路径时，可解析所有对应data文件
3. 优化结果报告展示
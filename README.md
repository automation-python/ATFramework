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
    # "casePath":"" 遍历所有脚本路径，执行所有脚本
    # "casePath":"***.data.yaml" 支持单个或多个.data.yaml文件，以，分隔
    # "casePath":"login,pay" 支持单个目录或多个目录遍历，执行目录下所有脚本
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

 1. 优化结果报告展示效果
 2. 优化脚本路径解析
 3. 新增压力测试

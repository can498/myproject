## case_generate模块说明

### 模型基类模块
- model: 包含所有定义的ecore文件
- ctc: 包含 CTC 相关类的定义信息，在生成CTC及参数时需要
- generator: 包含 generator 相关类的定义信息，在生成调用工具的JOB时或生成config文件时需要
- mapping: 包含 mapping 相关类的定义信息，生成.mapping文件时需要
- testcase: 包含 testcase 相关类的定义信息，生成.seq文件时需要

### 封装的工具模块
- utils:
  - load_model: 反序列化功能，将xml文件转化为python对象
  - save_model: 序列化功能，将python对象转化为xml文件

### UML图
- UML

### 示例代码。 
- demo:
  - generator_mapping: 生成mapping文件 .mapping 示例，具体内容参考代码内说明
  - generator_seq: 生成测试序列文件 .seq 示例，具体内容参考代码内说明

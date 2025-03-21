# 智能停车场管理系统 API 文档

本文档详细说明了智能停车场管理系统的API接口规范。

## 基本信息

- 基础URL: `http://localhost:5000/api`
- 响应格式: JSON
- 认证方式: JWT Token (在需要认证的接口中使用)

## 认证接口

### 登录

- **URL**: `/auth/login`
- **方法**: `POST`
- **描述**: 管理员登录
- **请求体**:
  ```json
  {
    "username": "admin",
    "password": "1234"
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
  ```
- **失败响应** (401):
  ```json
  {
    "success": false,
    "message": "用户名或密码错误"
  }
  ```

## 停车场管理接口

### 车辆入场

- **URL**: `/parking/entry`
- **方法**: `POST`
- **描述**: 记录车辆入场
- **请求体**:
  ```json
  {
    "plate_number": "京A12345",
    "plate_color": "蓝色"
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "message": "车辆 京A12345 成功入场",
    "record": {
      "id": 1,
      "plate_number": "京A12345",
      "plate_color": "蓝色",
      "entry_time": "2023-10-15T14:30:00"
    }
  }
  ```

### 车辆出场

- **URL**: `/parking/exit`
- **方法**: `POST`
- **描述**: 记录车辆出场并计算费用
- **请求体**:
  ```json
  {
    "plate_number": "京A12345"
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "message": "车辆 京A12345 成功出场",
    "record": {
      "id": 1,
      "plate_number": "京A12345",
      "entry_time": "2023-10-15T14:30:00",
      "exit_time": "2023-10-15T16:45:00",
      "parking_fee": 15.0
    },
    "fee_details": {
      "duration": 135,
      "duration_hours": 2.25,
      "rate": 10.0,
      "is_member": false,
      "discount": 1.0,
      "total_fee": 15.0
    }
  }
  ```

### 获取停车场状态

- **URL**: `/parking/status`
- **方法**: `GET`
- **描述**: 获取当前停车场状态
- **成功响应** (200):
  ```json
  {
    "success": true,
    "total_spaces": 100,
    "occupied_spaces": 45,
    "available_spaces": 55,
    "occupancy_rate": 45.0
  }
  ```

## 会员管理接口

### 获取会员列表

- **URL**: `/members`
- **方法**: `GET`
- **描述**: 获取所有会员信息
- **权限**: 需要管理员权限
- **请求头**: `Authorization: Bearer {token}`
- **成功响应** (200):
  ```json
  {
    "success": true,
    "members": [
      {
        "id": 1,
        "name": "张三",
        "plate_number": "京A12345",
        "phone": "13800138000",
        "status": "active",
        "created_at": "2023-09-01T10:00:00"
      },
      // ...更多会员
    ]
  }
  ```

### 添加会员

- **URL**: `/members`
- **方法**: `POST`
- **描述**: 添加新会员
- **权限**: 需要管理员权限
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "name": "李四",
    "plate_number": "京B54321",
    "phone": "13900139000",
    "status": "active"
  }
  ```
- **成功响应** (201):
  ```json
  {
    "success": true,
    "message": "会员添加成功",
    "member": {
      "id": 2,
      "name": "李四",
      "plate_number": "京B54321",
      "phone": "13900139000",
      "status": "active",
      "created_at": "2023-10-15T17:00:00"
    }
  }
  ```

## 更多接口文档请参考系统实现...

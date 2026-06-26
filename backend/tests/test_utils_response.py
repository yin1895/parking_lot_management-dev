"""测试 统一响应格式 (response.py)"""
import json
from backend.utils.response import api_success, api_error, api_paginated


class TestApiSuccess:
    def test_with_data(self):
        resp, code = api_success({"key": "val"}, "ok")
        data = json.loads(resp.get_data(as_text=True))
        assert code == 200
        assert data["success"] is True
        assert data["data"]["key"] == "val"
        assert data["message"] == "ok"

    def test_without_data(self):
        resp, code = api_success(message="no data")
        data = json.loads(resp.get_data(as_text=True))
        assert code == 200
        assert data["success"] is True
        assert "data" not in data

    def test_custom_status(self):
        resp, code = api_success(None, "created", 201)
        assert code == 201

    def test_none_data_excluded(self):
        resp, code = api_success()
        data = json.loads(resp.get_data(as_text=True))
        assert "data" not in data


class TestApiError:
    def test_basic(self):
        resp, code = api_error("出错了", 400)
        data = json.loads(resp.get_data(as_text=True))
        assert code == 400
        assert data["success"] is False
        assert data["message"] == "出错了"

    def test_with_errors(self):
        resp, code = api_error("校验失败", 422, {"name": "不能为空"})
        data = json.loads(resp.get_data(as_text=True))
        assert data["errors"]["name"] == "不能为空"

    def test_custom_status(self):
        resp, code = api_error("未找到", 404)
        assert code == 404


class TestApiPaginated:
    def test_basic_pagination(self):
        items = [{"id": i} for i in range(3)]
        resp, code = api_paginated(items, total=30, page=2, limit=3)
        data = json.loads(resp.get_data(as_text=True))
        assert code == 200
        assert data["success"] is True
        assert len(data["data"]) == 3
        assert data["pagination"]["total"] == 30
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["limit"] == 3
        assert data["pagination"]["pages"] == 10
        assert data["pagination"]["has_next"] is True
        assert data["pagination"]["has_prev"] is True

    def test_first_page(self):
        resp, code = api_paginated([], total=0, page=1, limit=20)
        data = json.loads(resp.get_data(as_text=True))
        assert data["pagination"]["pages"] == 1
        assert data["pagination"]["has_next"] is False
        assert data["pagination"]["has_prev"] is False

    def test_last_page(self):
        resp, code = api_paginated([{"id": 1}], total=11, page=11, limit=1)
        data = json.loads(resp.get_data(as_text=True))
        assert data["pagination"]["has_next"] is False
        assert data["pagination"]["has_prev"] is True

    def test_with_extra(self):
        resp, code = api_paginated([], total=0, page=1, limit=1, extra={"stats": {"x": 1}})
        data = json.loads(resp.get_data(as_text=True))
        assert data["stats"]["x"] == 1

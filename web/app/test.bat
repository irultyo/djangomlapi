@echo off
REM GET /api/home
echo ==========================
echo GET /api/home
echo ==========================
curl -X GET "http://192.168.1.103:8001/api/home"
echo.

REM POST /api/retrieve
echo ==========================
echo POST /api/retrieve
echo ==========================
curl -X POST "http://192.168.1.103:8001/api/retrieve" -H "Content-Type: application/json" -d "{\"index\": 1}"
echo.

REM POST /api/generate
echo ==========================
echo POST /api/generate
echo ==========================
curl -X POST "http://192.168.1.103:8001/api/generate" -H "Content-Type: application/json" -d "{\"patch_a\": 1, \"patch_b\": 2, \"model\": [\"batikgan_cl\", \"batikgan_sl\"]}"
echo.

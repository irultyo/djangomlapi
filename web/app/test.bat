@echo off

set url="https://batik.umm.ac.id/batik_product/28"
REM GET /api/home
echo ==========================
echo GET /api/home
echo ==========================
curl -X GET "%url%/api/home"
echo.

REM POST /api/retrieve
echo ==========================
echo POST /api/retrieve
echo ==========================
curl -X POST "%url%/api/retrieve" -H "Content-Type: application/json" -d "{\"index\": 119}"
echo.

REM POST /api/generate
echo ==========================
echo POST /api/generate
echo ==========================
curl -X POST "%url%/api/generate" -H "Content-Type: application/json" -d "{\"patch_a\": 1, \"patch_b\": 2, \"model\": [\"batikgan_cl\", \"batikgan_sl\"]}"
echo.

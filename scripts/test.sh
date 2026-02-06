#!/bin/bash

# Test script for framebox
# Run this after starting the server with: python main.py

set -e

API_BASE="${API_BASE:-http://localhost:8000}"
PROJECT_NAME="test-project-$(date +%s)"
PROJECT_ID=""

echo "=== framebox Test Suite ==="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test helper
test_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1${NC}"
        exit 1
    fi
}

# 1. Test health check
echo "1. Testing health check..."
curl -s "$API_BASE/api/health" > /dev/null
test_result "Health check endpoint"

# 2. Test project creation
echo ""
echo "2. Testing project creation..."
RESPONSE=$(curl -s -X POST "$API_BASE/api/projects" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$PROJECT_NAME\", \"entry_file\": \"index.html\"}")

PROJECT_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -n "$PROJECT_ID" ]; then
    echo "   Created project ID: $PROJECT_ID"
    test_result "Project creation"
else
    echo "   Failed to create project"
    echo "   Response: $RESPONSE"
    exit 1
fi

# 3. Test duplicate name rejection
echo ""
echo "3. Testing duplicate name rejection..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/api/projects" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$PROJECT_NAME\"}")

if [ "$HTTP_CODE" = "409" ]; then
    test_result "Duplicate name rejection (409)"
else
    echo "   Expected 409, got $HTTP_CODE"
    exit 1
fi

# 4. Test list projects
echo ""
echo "4. Testing list projects..."
curl -s "$API_BASE/api/projects" | grep -q "$PROJECT_NAME"
test_result "List projects"

# 5. Test get project by ID
echo ""
echo "5. Testing get project by ID..."
curl -s "$API_BASE/api/projects/$PROJECT_ID" | grep -q "$PROJECT_NAME"
test_result "Get project by ID"

# 6. Test get project by name
echo ""
echo "6. Testing get project by name..."
curl -s "$API_BASE/api/projects/$PROJECT_NAME" | grep -q "$PROJECT_ID"
test_result "Get project by name"

# 7. Test file upload - create test files
echo ""
echo "7. Testing file upload..."
mkdir -p /tmp/iframe-test
cat > /tmp/iframe-test/index.html <<EOF
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Test Project</h1>
<script src="./script.js"></script>
</body>
</html>
EOF

cat > /tmp/iframe-test/data.json <<EOF
{"message": "Hello from framebox!"}
EOF

mkdir -p /tmp/iframe-test/assets
cat > /tmp/iframe-test/assets/style.css <<EOF
body { background: #f0f0f0; }
EOF

# Upload files
curl -s -X POST "$API_BASE/api/projects/$PROJECT_ID/files" \
    -F "files=@/tmp/iframe-test/index.html" \
    -F "files=@/tmp/iframe-test/data.json" \
    -F "files=@/tmp/iframe-test/assets/style.css;filename=assets/style.css" \
    > /dev/null

test_result "File upload (batch with nested path)"

# 8. Test list project files
echo ""
echo "8. Testing list project files..."
FILES=$(curl -s "$API_BASE/api/projects/$PROJECT_ID/files")
echo "$FILES" | grep -q "index.html" && \
echo "$FILES" | grep -q "data.json" && \
echo "$FILES" | grep -q "assets/style.css"
test_result "List project files"

# 9. Test static serving - entry file by ID
echo ""
echo "9. Testing static serving (entry file by ID)..."
curl -s "$API_BASE/view/$PROJECT_ID/" | grep -q "Test Project"
test_result "Serve entry file by ID"

# 10. Test static serving - entry file by name
echo ""
echo "10. Testing static serving (entry file by name)..."
curl -s "$API_BASE/view/$PROJECT_NAME/" | grep -q "Test Project"
test_result "Serve entry file by name"

# 11. Test static serving - nested file
echo ""
echo "11. Testing static serving (nested file)..."
curl -s "$API_BASE/view/$PROJECT_ID/assets/style.css" | grep -q "background"
test_result "Serve nested file"

# 12. Test static serving - JSON file
echo ""
echo "12. Testing static serving (JSON file)..."
curl -s "$API_BASE/view/$PROJECT_ID/data.json" | grep -q "Hello from framebox"
test_result "Serve JSON file"

# 13. Test CORS headers
echo ""
echo "13. Testing CORS headers..."
HEADERS=$(curl -s -v "$API_BASE/view/$PROJECT_ID/" 2>&1 | grep -i "access-control")
if [ -n "$HEADERS" ]; then
    test_result "CORS headers present"
else
    echo "No CORS headers found"
    exit 1
fi

# 14. Test path validation (should reject ..)
echo ""
echo "14. Testing path validation (directory traversal)..."
cat > /tmp/iframe-test/malicious.txt <<EOF
../../etc/passwd
EOF

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/api/projects/$PROJECT_ID/files" \
    -F "files=@/tmp/iframe-test/malicious.txt;filename=../../../etc/passwd")

if [ "$HTTP_CODE" = "400" ]; then
    test_result "Path validation (reject ..)"
else
    echo "   Expected 400, got $HTTP_CODE"
    exit 1
fi

# 15. Test project update
echo ""
echo "15. Testing project update..."
curl -s -X PUT "$API_BASE/api/projects/$PROJECT_ID" \
    -H "Content-Type: application/json" \
    -d '{"entry_file": "main.html"}' > /dev/null
test_result "Project update"

# 16. Test search functionality
echo ""
echo "16. Testing search functionality..."
curl -s "$API_BASE/api/projects?search=test-project" | grep -q "$PROJECT_NAME"
test_result "Search projects"

# 17. Test project deletion
echo ""
echo "17. Testing project deletion..."
curl -s -X DELETE "$API_BASE/api/projects/$PROJECT_ID" > /dev/null
test_result "Project deletion"

# 18. Verify project is deleted
echo ""
echo "18. Verifying project is deleted..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/api/projects/$PROJECT_ID")

if [ "$HTTP_CODE" = "404" ]; then
    test_result "Project deleted (404)"
else
    echo "   Expected 404, got $HTTP_CODE"
    exit 1
fi

# Cleanup
rm -rf /tmp/iframe-test

echo ""
echo "==================================="
echo -e "${GREEN}All tests passed! ✓${NC}"
echo "==================================="

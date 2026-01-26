#!/bin/bash
# Test all Meta-Meme URLs for backward compatibility

set -e

BASE_URL="https://meta-meme-dev.jmikedupont2.workers.dev"
PROD_URL="https://meta-meme.jmikedupont2.workers.dev"

echo "🧪 Testing Meta-Meme URLs"
echo "=========================="
echo ""

# Test function
test_url() {
    local name="$1"
    local url="$2"
    local expected="${3:-200}"
    
    echo -n "Testing $name... "
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    time=$(curl -s -o /dev/null -w "%{time_total}" "$url")
    
    if [ "$status" = "$expected" ]; then
        echo "✅ $status (${time}s)"
        return 0
    else
        echo "❌ $status (expected $expected)"
        return 1
    fi
}

echo "📍 DEV Environment"
echo "---"

# Old RDFa compressed URL
test_url "Old RDFa (compressed)" \
    "${BASE_URL}?compressed=H4sIANeAdmkC_6WS0WqDMBSG7_ceXq5ootbCGC1ju9kKg22wq0JmTzXMmJBGrHv6pdMWXR1rcyTgUc7_JZ_HudKw4TuP-KLagkcXtrrJjVE_5YNdAgy7FiBgInW2f973EXprGyeev5gfAV-f58Rt11g4F2dtvm8bi--267F4XdeTmnZZ4vuBvb0vn17SHATrgezq9O9YUXCp4OCTSiG4EVAa-8Yj9gpnySyy1WrVbspLAxnojvQHRmkpNy2BJiRMSHAJov04UKa6UQbWLScOSRgFCYn_BVkMVqeHcFFp4ziNe80M1mPAcBA55JEmlQGN_sV-UVxsjgSczxIKJe35sUYnHAenPgNn9SyLJm9EyRlS6xTk4DWA4MRe7dC3PM2lxg5shOSgNqQg3XJWoAc2hLgYHQA4mTfN-vNmWaYhYwZaTEBncRBGU3ohRlUfBU8foelOE0V0Oo64-gazriywHQgAAA=="

# New consultation URL (Urania + Lean4)
test_url "Consultation (Urania+Lean4)" \
    "${BASE_URL}?consult=eyJtdXNlIjoiVXJhbmlhIiwidG9vbCI6ImxlYW40IiwicXVlcnkiOiJWZXJpZnkgZWlnZW52ZWN0b3IgY29udmVyZ2VuY2UiLCJjb250ZXh0IjoiOCEgPSA0MCwzMjAgcmVmbGVjdGlvbnMifQ=="

# New LLM prompt URL (Calliope + LLM)
test_url "LLM Prompt (Calliope+LLM)" \
    "${BASE_URL}?llm=eyJtdXNlIjoiQ2FsbGlvcGUiLCJ0b29sIjoibGxtIiwicXVlcnkiOiJHZW5lcmF0ZSBhIHBvZW0gYWJvdXQgbWV0YS1tZW1lcyIsImNvbnRleHQiOiJGb3JtYWxseSB2ZXJpZmllZCBBSS1odW1hbiBjcmVhdGl2aXR5In0="

# Direct RDFa access
test_url "Direct RDFa (/rdfa)" \
    "${BASE_URL}/rdfa"

# Default page (consultation)
test_url "Default page" \
    "${BASE_URL}/"

echo ""
echo "📍 PRODUCTION Environment"
echo "---"

# Old RDFa compressed URL
test_url "Old RDFa (compressed)" \
    "${PROD_URL}?compressed=H4sIANeAdmkC_6WS0WqDMBSG7_ceXq5ootbCGC1ju9kKg22wq0JmTzXMmJBGrHv6pdMWXR1rcyTgUc7_JZ_HudKw4TuP-KLagkcXtrrJjVE_5YNdAgy7FiBgInW2f973EXprGyeev5gfAV-f58Rt11g4F2dtvm8bi--267F4XdeTmnZZ4vuBvb0vn17SHATrgezq9O9YUXCp4OCTSiG4EVAa-8Yj9gpnySyy1WrVbspLAxnojvQHRmkpNy2BJiRMSHAJov04UKa6UQbWLScOSRgFCYn_BVkMVqeHcFFp4ziNe80M1mPAcBA55JEmlQGN_sV-UVxsjgSczxIKJe35sUYnHAenPgNn9SyLJm9EyRlS6xTk4DWA4MRe7dC3PM2lxg5shOSgNqQg3XJWoAc2hLgYHQA4mTfN-vNmWaYhYwZaTEBncRBGU3ohRlUfBU8foelOE0V0Oo64-gazriywHQgAAA=="

# New consultation URL
test_url "Consultation (Urania+Lean4)" \
    "${PROD_URL}?consult=eyJtdXNlIjoiVXJhbmlhIiwidG9vbCI6ImxlYW40IiwicXVlcnkiOiJWZXJpZnkgZWlnZW52ZWN0b3IgY29udmVyZ2VuY2UiLCJjb250ZXh0IjoiOCEgPSA0MCwzMjAgcmVmbGVjdGlvbnMifQ=="

# Default page
test_url "Default page" \
    "${PROD_URL}/"

echo ""
echo "✅ All tests passed!"
echo ""
echo "📊 Summary:"
echo "  - Old RDFa URLs: Working (?compressed=...)"
echo "  - New Consultation URLs: Working (?consult=...)"
echo "  - LLM Prompt URLs: Working (?llm=...)"
echo "  - Direct RDFa: Working (/rdfa)"
echo "  - Backward compatibility: ✅ Verified"

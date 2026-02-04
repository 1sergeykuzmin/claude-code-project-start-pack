#!/bin/bash
# Cleanup Dialogs
# Redact credentials from exported dialog files
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
DIALOG_DIR="${1:-dialog}"
DRY_RUN=false
BACKUP=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-backup)
            BACKUP=false
            shift
            ;;
        *)
            DIALOG_DIR="$1"
            shift
            ;;
    esac
done

echo "=================================="
echo "Dialog Credential Cleanup"
echo "=================================="
echo ""
echo "Directory: $DIALOG_DIR"
echo "Dry run: $DRY_RUN"
echo ""

# Check if dialog directory exists
if [ ! -d "$DIALOG_DIR" ]; then
    echo -e "${YELLOW}Dialog directory not found: $DIALOG_DIR${NC}"
    echo "Nothing to clean."
    exit 0
fi

# Patterns to redact
REDACT_PATTERNS=(
    # API Keys
    's/sk-[a-zA-Z0-9]{32,}/[REDACTED_API_KEY]/g'
    's/sk_live_[a-zA-Z0-9]+/[REDACTED_STRIPE_KEY]/g'
    's/sk_test_[a-zA-Z0-9]+/[REDACTED_STRIPE_KEY]/g'
    's/pk_live_[a-zA-Z0-9]+/[REDACTED_STRIPE_KEY]/g'
    's/pk_test_[a-zA-Z0-9]+/[REDACTED_STRIPE_KEY]/g'

    # GitHub tokens
    's/ghp_[a-zA-Z0-9]{36}/[REDACTED_GITHUB_TOKEN]/g'
    's/gho_[a-zA-Z0-9]{36}/[REDACTED_GITHUB_TOKEN]/g'
    's/ghu_[a-zA-Z0-9]{36}/[REDACTED_GITHUB_TOKEN]/g'
    's/ghs_[a-zA-Z0-9]{36}/[REDACTED_GITHUB_TOKEN]/g'

    # AWS
    's/AKIA[0-9A-Z]{16}/[REDACTED_AWS_KEY]/g'
    's/aws_secret_access_key\s*[:=]\s*['\''"][^'\''"]+['\''"]/ aws_secret_access_key = "[REDACTED]"/g'

    # Generic patterns
    's/password\s*[:=]\s*['\''"][^'\''"]+['\''"]/ password = "[REDACTED]"/g'
    's/api_key\s*[:=]\s*['\''"][^'\''"]+['\''"]/ api_key = "[REDACTED]"/g'
    's/apiKey\s*[:=]\s*['\''"][^'\''"]+['\''"]/ apiKey = "[REDACTED]"/g'
    's/secret\s*[:=]\s*['\''"][^'\''"]+['\''"]/ secret = "[REDACTED]"/g'
    's/token\s*[:=]\s*['\''"][^'\''"]+['\''"]/ token = "[REDACTED]"/g'

    # Bearer tokens
    's/Bearer [a-zA-Z0-9\._-]+/Bearer [REDACTED]/g'

    # Basic auth
    's/Basic [a-zA-Z0-9+\/=]+/Basic [REDACTED]/g'

    # Private keys
    's/-----BEGIN [A-Z]+ PRIVATE KEY-----/[REDACTED_PRIVATE_KEY]/g'
    's/-----BEGIN RSA PRIVATE KEY-----/[REDACTED_PRIVATE_KEY]/g'
)

TOTAL_FILES=0
CLEANED_FILES=0
TOTAL_REDACTIONS=0

# Find all markdown files in dialog directory
while IFS= read -r -d '' file; do
    ((TOTAL_FILES++))

    file_redactions=0

    # Check each pattern
    for pattern in "${REDACT_PATTERNS[@]}"; do
        # Count matches
        matches=$(grep -c -E "$(echo "$pattern" | sed 's/s\///' | sed 's/\/.*$//')" "$file" 2>/dev/null || echo "0")
        file_redactions=$((file_redactions + matches))
    done

    if [ $file_redactions -gt 0 ]; then
        ((CLEANED_FILES++))
        TOTAL_REDACTIONS=$((TOTAL_REDACTIONS + file_redactions))

        echo -e "${YELLOW}Found $file_redactions potential credential(s) in: $file${NC}"

        if [ "$DRY_RUN" = false ]; then
            # Create backup if enabled
            if [ "$BACKUP" = true ]; then
                cp "$file" "${file}.bak"
            fi

            # Apply redactions
            for pattern in "${REDACT_PATTERNS[@]}"; do
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    sed -i '' -E "$pattern" "$file" 2>/dev/null || true
                else
                    # Linux
                    sed -i -E "$pattern" "$file" 2>/dev/null || true
                fi
            done

            echo -e "  ${GREEN}✓ Redacted${NC}"
        else
            echo "  (dry run - no changes made)"
        fi
    fi
done < <(find "$DIALOG_DIR" -name "*.md" -type f -print0 2>/dev/null)

# Summary
echo ""
echo "=================================="
echo "Summary"
echo "=================================="
echo "Files scanned: $TOTAL_FILES"
echo "Files with credentials: $CLEANED_FILES"
echo "Total redactions: $TOTAL_REDACTIONS"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "This was a dry run. No files were modified."
    echo "Run without --dry-run to apply changes."
fi

if [ $CLEANED_FILES -gt 0 ] && [ "$DRY_RUN" = false ]; then
    echo ""
    echo -e "${GREEN}Cleanup complete.${NC}"
    if [ "$BACKUP" = true ]; then
        echo "Backups created with .bak extension."
    fi
fi

exit 0

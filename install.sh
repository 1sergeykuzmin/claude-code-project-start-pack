#!/bin/bash
#
# Claude Code Project Framework - Installer
# https://github.com/1sergeykuzmin/claude-code-project-start-pack
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack/main/install.sh | bash
#
# Or download and run with options:
#   ./install.sh --dry-run    # Preview installation
#   ./install.sh --minimal    # Only .claude/ directory
#   ./install.sh --update     # Update existing installation
#

set -e

# ============================================================================
# Configuration
# ============================================================================

REPO_URL="https://github.com/1sergeykuzmin/claude-code-project-start-pack"
REPO_RAW="https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack"
BRANCH="main"
VERSION="2.0.0"
TMP_DIR="/tmp/claude-framework-$$"

# ============================================================================
# Flags (defaults)
# ============================================================================

FLAG_MINIMAL=false
FLAG_FORCE=false
FLAG_NO_HOOKS=false
FLAG_UPDATE=false
FLAG_DRY_RUN=false
FLAG_HELP=false

# ============================================================================
# Colors and Output
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}$1${NC}"
}

log_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "  ${YELLOW}!${NC} $1"
}

log_error() {
    echo -e "  ${RED}✗${NC} $1"
}

log_step() {
    echo -e "\n${BOLD}$1${NC}"
}

# ============================================================================
# Help
# ============================================================================

show_help() {
    cat << EOF
Claude Code Project Framework - Installer v${VERSION}

Usage: install.sh [OPTIONS]

Options:
  --minimal     Only install .claude/ directory (no src/, security/)
  --force       Overwrite existing files without prompts
  --no-hooks    Skip git hooks installation
  --update      Update mode - refresh framework, preserve customizations
  --dry-run     Show what would be done without doing it
  --help        Show this help message

Examples:
  # Full installation
  ./install.sh

  # Preview what will be installed
  ./install.sh --dry-run

  # Minimal installation (just commands and protocols)
  ./install.sh --minimal

  # Update existing installation
  ./install.sh --update --force

One-liner installation:
  curl -fsSL ${REPO_RAW}/main/install.sh | bash

Documentation: ${REPO_URL}
EOF
}

# ============================================================================
# Argument Parsing
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --minimal)
                FLAG_MINIMAL=true
                shift
                ;;
            --force)
                FLAG_FORCE=true
                shift
                ;;
            --no-hooks)
                FLAG_NO_HOOKS=true
                shift
                ;;
            --update)
                FLAG_UPDATE=true
                shift
                ;;
            --dry-run)
                FLAG_DRY_RUN=true
                shift
                ;;
            --help|-h)
                FLAG_HELP=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

# ============================================================================
# Prerequisites
# ============================================================================

check_prerequisites() {
    log_step "Checking prerequisites..."

    local has_error=false

    # Check git
    if command -v git &> /dev/null; then
        log_success "git found"
    else
        log_error "git not found (required)"
        has_error=true
    fi

    # Check python3
    if command -v python3 &> /dev/null; then
        local py_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        log_success "python3 found ($py_version)"
    else
        log_warning "python3 not found (optional, needed for parallel execution)"
    fi

    # Check if in git repo
    if git rev-parse --git-dir &> /dev/null; then
        log_success "Git repository detected"
    else
        log_warning "Not a git repository (git hooks won't be installed)"
        FLAG_NO_HOOKS=true
    fi

    if $has_error; then
        echo ""
        log_error "Prerequisites check failed. Please install missing dependencies."
        exit 1
    fi
}

# ============================================================================
# Download
# ============================================================================

download_framework() {
    log_step "Downloading framework..."

    if $FLAG_DRY_RUN; then
        log_info "  Would clone ${REPO_URL} to ${TMP_DIR}"
        return
    fi

    # Cleanup on exit
    trap cleanup EXIT

    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TMP_DIR" 2>/dev/null
    log_success "Cloned from github.com/1sergeykuzmin/claude-code-project-start-pack"
}

cleanup() {
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
}

# ============================================================================
# Backup
# ============================================================================

backup_existing() {
    if [[ -d ".claude" ]] && ! $FLAG_FORCE && ! $FLAG_UPDATE; then
        log_step "Existing installation detected..."

        if $FLAG_DRY_RUN; then
            log_info "  Would backup .claude/ to .claude.backup/"
            return
        fi

        echo ""
        echo "  An existing .claude/ directory was found."
        echo "  Options:"
        echo "    1) Backup and continue (recommended)"
        echo "    2) Overwrite without backup"
        echo "    3) Cancel installation"
        echo ""
        read -p "  Choose [1/2/3]: " choice

        case $choice in
            1)
                local backup_dir=".claude.backup.$(date +%Y%m%d%H%M%S)"
                cp -r .claude "$backup_dir"
                log_success "Backed up to $backup_dir"
                ;;
            2)
                log_warning "Proceeding without backup"
                ;;
            *)
                echo "Installation cancelled."
                exit 0
                ;;
        esac
    fi
}

# ============================================================================
# Installation Functions
# ============================================================================

copy_claude_dir() {
    log_step "Installing framework files..."

    if $FLAG_DRY_RUN; then
        log_info "  Would copy .claude/ (commands, protocols, skills, config)"
        return
    fi

    # If update mode, preserve custom commands
    if $FLAG_UPDATE && [[ -d ".claude/commands" ]]; then
        # Backup custom commands
        local custom_commands=$(find .claude/commands -name "*.md" -newer "$TMP_DIR/.claude/commands" 2>/dev/null || true)
        if [[ -n "$custom_commands" ]]; then
            mkdir -p /tmp/claude-custom-$$
            for cmd in $custom_commands; do
                cp "$cmd" /tmp/claude-custom-$$/
            done
        fi
    fi

    # Copy .claude directory
    cp -r "$TMP_DIR/.claude" ./

    # Restore custom commands in update mode
    if $FLAG_UPDATE && [[ -d "/tmp/claude-custom-$$" ]]; then
        cp /tmp/claude-custom-$$/* .claude/commands/ 2>/dev/null || true
        rm -rf /tmp/claude-custom-$$
    fi

    # Count what was installed
    local cmd_count=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    local proto_count=$(find .claude/protocols -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    local skill_count=$(find .claude/skills -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    skill_count=$((skill_count - 1)) # Subtract the skills dir itself

    log_success "Copied .claude/ (${cmd_count} commands, ${proto_count} protocols, ${skill_count} skills)"
}

copy_framework_core() {
    if $FLAG_MINIMAL; then
        log_warning "Skipped src/framework-core/ (--minimal mode)"
        return
    fi

    if $FLAG_DRY_RUN; then
        log_info "  Would copy src/framework-core/"
        return
    fi

    mkdir -p src
    cp -r "$TMP_DIR/src/framework-core" ./src/
    log_success "Copied src/framework-core/"
}

copy_security() {
    if $FLAG_MINIMAL; then
        log_warning "Skipped security/ (--minimal mode)"
        return
    fi

    if $FLAG_DRY_RUN; then
        log_info "  Would copy security/"
        return
    fi

    cp -r "$TMP_DIR/security" ./
    log_success "Copied security/"
}

setup_dev_docs() {
    if $FLAG_DRY_RUN; then
        log_info "  Would create dev-docs/ structure"
        return
    fi

    mkdir -p dev-docs

    # Create empty files if they don't exist
    for f in prd.md trd.md to-do.md; do
        if [[ ! -f "dev-docs/$f" ]]; then
            touch "dev-docs/$f"
        fi
    done

    # Copy templates if files are empty or don't exist
    if [[ ! -s "dev-docs/snapshot.md" ]]; then
        cp "$TMP_DIR/dev-docs/snapshot.md" ./dev-docs/ 2>/dev/null || touch dev-docs/snapshot.md
    fi

    if [[ ! -s "dev-docs/architecture.md" ]]; then
        cp "$TMP_DIR/dev-docs/architecture.md" ./dev-docs/ 2>/dev/null || touch dev-docs/architecture.md
    fi

    log_success "Created dev-docs/ structure"
}

# ============================================================================
# Merging Functions
# ============================================================================

merge_claude_md() {
    if $FLAG_DRY_RUN; then
        if [[ -f "CLAUDE.md" ]]; then
            log_info "  Would merge framework into existing CLAUDE.md"
        else
            log_info "  Would create CLAUDE.md"
        fi
        return
    fi

    if [[ -f "CLAUDE.md" ]]; then
        # Check if framework section already exists
        if grep -q "Claude Code Project Framework" CLAUDE.md 2>/dev/null; then
            if $FLAG_UPDATE || $FLAG_FORCE; then
                # Remove old framework section and re-add
                # Keep everything before the framework section
                sed -n '/^# Claude Code Project Framework/q;p' CLAUDE.md > CLAUDE.md.tmp
                echo "" >> CLAUDE.md.tmp
                echo "---" >> CLAUDE.md.tmp
                echo "" >> CLAUDE.md.tmp
                cat "$TMP_DIR/CLAUDE.md" >> CLAUDE.md.tmp
                mv CLAUDE.md.tmp CLAUDE.md
                log_success "Updated CLAUDE.md (refreshed framework section)"
            else
                log_warning "CLAUDE.md already has framework section (use --update to refresh)"
            fi
        else
            # Append framework section
            echo "" >> CLAUDE.md
            echo "---" >> CLAUDE.md
            echo "" >> CLAUDE.md
            cat "$TMP_DIR/CLAUDE.md" >> CLAUDE.md
            log_success "Merged CLAUDE.md (preserved existing content)"
        fi
    else
        cp "$TMP_DIR/CLAUDE.md" ./
        log_success "Created CLAUDE.md"
    fi
}

merge_gitignore() {
    if $FLAG_DRY_RUN; then
        log_info "  Would update .gitignore with framework patterns"
        return
    fi

    local patterns=(
        "# Claude Code Framework"
        ".claude/.framework-config"
        ".claude/.framework-log"
        ".claude/.last_session"
        ""
        "# Dialog exports (may contain sensitive information)"
        "dialog/*.md"
        "!dialog/README.md"
    )

    # Check if patterns already exist
    if [[ -f ".gitignore" ]] && grep -q "Claude Code Framework" .gitignore 2>/dev/null; then
        log_warning ".gitignore already has framework patterns"
        return
    fi

    # Append patterns
    echo "" >> .gitignore
    for pattern in "${patterns[@]}"; do
        echo "$pattern" >> .gitignore
    done

    log_success "Updated .gitignore"
}

# ============================================================================
# Git Hooks
# ============================================================================

install_git_hooks() {
    if $FLAG_NO_HOOKS; then
        log_warning "Skipped git hooks (--no-hooks or not a git repo)"
        return
    fi

    if $FLAG_DRY_RUN; then
        log_info "  Would install git hooks"
        return
    fi

    if [[ -f ".claude/scripts/install-git-hooks.sh" ]]; then
        chmod +x .claude/scripts/install-git-hooks.sh
        .claude/scripts/install-git-hooks.sh > /dev/null 2>&1
        log_success "Installed git hooks"
    else
        log_warning "Git hooks script not found"
    fi
}

# ============================================================================
# Summary
# ============================================================================

show_summary() {
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"

    if $FLAG_DRY_RUN; then
        echo -e "${BOLD}║              Dry Run Complete (no changes made)              ║${NC}"
    else
        echo -e "${BOLD}║                    Installation Complete!                     ║${NC}"
    fi

    echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if ! $FLAG_DRY_RUN; then
        echo -e "${BOLD}Next steps:${NC}"
        echo "  1. Review CLAUDE.md and customize for your project"
        echo "  2. Run /migrate-legacy to analyze existing code"
        echo "     Or start fresh with /prd <your idea>"
        echo "  3. Begin a session with: start"
        echo ""
        echo -e "${BOLD}Quick start:${NC}"
        echo "  claude    # Launch Claude Code"
        echo "  start     # Begin a session"
        echo ""
    fi

    echo -e "Documentation: ${BLUE}${REPO_URL}${NC}"
}

# ============================================================================
# Main
# ============================================================================

main() {
    parse_args "$@"

    if $FLAG_HELP; then
        show_help
        exit 0
    fi

    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║     Claude Code Project Framework - Installer v${VERSION}           ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"

    if $FLAG_DRY_RUN; then
        echo -e "\n${YELLOW}DRY RUN MODE - No changes will be made${NC}"
    fi

    check_prerequisites
    backup_existing
    download_framework
    copy_claude_dir
    copy_framework_core
    copy_security
    setup_dev_docs
    merge_claude_md
    merge_gitignore
    install_git_hooks
    show_summary
}

main "$@"

#!/bin/bash
# GitHub PR Creation Script - Enterprise Security Hardening
# Run this to create and push the PR for Phase 1 P0 fixes

set -e

# Configuration
BRANCH_NAME="feature/enterprise-security-hardening-p0"
PR_TITLE="[P0] Enterprise Security & Data Persistence Hardening - Phase 1"
MAIN_BRANCH="main"

echo "🚀 Creating PR for Enterprise Security Hardening (Phase 1)"
echo "=============================================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install git first."
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $CURRENT_BRANCH"

# Create feature branch
echo "📝 Creating feature branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME" || git checkout "$BRANCH_NAME"

# Stage all changes
echo "📦 Staging changes..."
git add -A

# Show what's being committed
echo ""
echo "📋 Changes to be committed:"
git status --short

# Commit changes
echo ""
echo "💾 Committing changes..."
git commit -m "[$BRANCH_NAME] Phase 1 Critical Security & Data Persistence Fixes

## Changes

### Security Hardening (P0)
- Removed hardcoded demo credentials
- Implemented account lockout (5 attempts → 30-minute lockout)
- Added NIST SP 800-63B compliant password validation
- Implemented rate limiting for authentication
- Enhanced user schema with security tracking fields
- Created comprehensive audit logging system
- Added structured logging with file rotation

### Data Persistence (P0)
- Fixed database_manager stub functions
- Implemented real assessment data persistence
- Added assessments, responses, and domain_scores tables
- Created database indexes for performance
- Full assessment history retrieval

### Code Quality (P0)
- Removed duplicate scoring functions
- Standardized maturity level scale
- Updated authentication components for security

### Dependencies & Configuration (P1)
- Pinned all package versions for reproducibility
- Added missing packages (bcrypt, python-dotenv, pydantic)
- Created .env.example configuration template

## Files Modified
- src/modules/auth/auth_manager.py
- src/modules/auth/auth_components.py
- src/modules/data/database_manager.py
- src/modules/assessment/scoring_engine.py
- requirements.txt

## Files Created
- src/config/logging_config.py
- src/modules/utils/audit_logger.py
- src/modules/utils/password_validator.py
- src/modules/utils/rate_limiter.py
- .env.example
- PHASE_1_CHANGES.md

## Breaking Changes
- Demo login credentials removed (security requirement)
- Users must create real accounts
- Stronger password requirements

## Testing
- [ ] Password validation with various inputs
- [ ] Rate limiting after 5 failed attempts
- [ ] Assessment persistence across sessions
- [ ] Audit log creation for all events

## Compliance Impact
- ✅ NIST SP 800-63B (password policy)
- ✅ SOC 2 (audit trail)
- ✅ GDPR foundation (user tracking)
- ✅ ISO 27001 foundation (access control, logging)

See PHASE_1_CHANGES.md for detailed information."

# Push to remote
echo ""
echo "🌐 Pushing to remote repository..."
git push -u origin "$BRANCH_NAME"

# Create PR (requires GitHub CLI)
if command -v gh &> /dev/null; then
    echo ""
    echo "📤 Creating GitHub Pull Request..."
    gh pr create \
        --title "$PR_TITLE" \
        --body "See PHASE_1_CHANGES.md for detailed information about Phase 1 P0 critical fixes." \
        --base "$MAIN_BRANCH" \
        --head "$BRANCH_NAME" \
        --reviewer "Adrian-Obungu" \
        --draft
    
    echo "✅ PR created successfully!"
else
    echo ""
    echo "⚠️  GitHub CLI (gh) not found. Please create PR manually:"
    echo "   1. Go to: https://github.com/Adrian-Obungu/AI-governance-assessor"
    echo "   2. Create Pull Request from '$BRANCH_NAME' to '$MAIN_BRANCH'"
    echo "   3. Use the commit message as PR description"
fi

echo ""
echo "✅ Done! Phase 1 changes are ready for review."
echo "📖 See PHASE_1_CHANGES.md for complete change documentation."

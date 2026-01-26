# Standard Operating Procedure: Cloudflare Workers Builds

**Version:** 1.0  
**Last Updated:** 2026-01-26  
**Purpose:** Deploy Workers to Cloudflare using Git integration and automated builds

---

## 1. Prerequisites

### 1.1 Required Access
- Cloudflare account with Workers access
- GitHub or GitLab repository access
- API token with appropriate permissions

### 1.2 Required Files
- `wrangler.toml` or `wrangler.jsonc` configuration file
- Worker source code (JavaScript/TypeScript)
- `package.json` with Wrangler dependency

---

## 2. Initial Setup

### 2.1 Connect New Worker to Git Repository

**Steps:**
1. Navigate to [Cloudflare Dashboard → Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers-and-pages)
2. Click **Create application**
3. Select **Get started** next to **Import a repository**
4. Choose **Git account** (GitHub or GitLab)
5. Select repository from list or use search
6. Configure project settings (see Section 3)
7. Click **Save and Deploy**
8. Verify deployment at `<worker-name>.workers.dev`

### 2.2 Connect Existing Worker to Git Repository

**Steps:**
1. Navigate to [Cloudflare Dashboard → Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers-and-pages)
2. Select existing Worker
3. Go to **Settings** → **Builds**
4. Click **Connect**
5. Follow prompts to connect repository
6. Configure build settings (see Section 3)
7. Push commit to trigger first build

**⚠️ Critical Requirement:**
- Worker name in dashboard MUST match `name` field in `wrangler.toml`
- Mismatch will cause build failure

---

## 3. Build Configuration

### 3.1 Core Settings

Navigate to **Settings** → **Builds** to configure:

| Setting | Description | Example |
|---------|-------------|---------|
| **Git account** | GitHub or GitLab account | `meta-introspector` |
| **Git repository** | Repository to monitor | `meta-meme` |
| **Git branch** | Branch to deploy from | `main` or `unified-memes` |
| **Root directory** | Project path (for monorepos) | `.` or `workers/my-worker` |
| **Build command** | Pre-deployment build step | `npm run build` |
| **Deploy command** | Wrangler deployment command | `npx wrangler deploy` |
| **Non-prod deploy command** | Command for preview branches | `npx wrangler versions upload` |

### 3.2 Deploy Command Options

**Standard deployment:**
```bash
npx wrangler deploy
```

**With static assets:**
```bash
npx wrangler deploy --assets /public/
```

**With environment:**
```bash
npx wrangler deploy --env staging
```

**Using package.json script:**
```bash
npm run deploy
```

### 3.3 Non-Production Branch Deployment

**Default (creates preview URL):**
```bash
npx wrangler versions upload
```

**With environment:**
```bash
npx wrangler versions upload --env staging
```

**Alternative package manager:**
```bash
yarn exec wrangler versions upload
```

---

## 4. API Token Configuration

### 4.1 Auto-Generated Token (Recommended)

Cloudflare automatically creates a token with required permissions:
- **Account:** Account Settings (read), Workers Scripts (edit), Workers KV (edit), R2 (edit)
- **Zone:** Workers Routes (edit) for all zones
- **User:** User Details (read), Memberships (read)

### 4.2 Custom Token

**Steps:**
1. Go to **My Profile** → **API Tokens**
2. Create token with permissions listed above
3. In Worker settings, select custom token
4. Use same token for all deployments to maintain consistent permissions

---

## 5. Environment Variables

### 5.1 Build-Time Variables

**Via Dashboard:**
1. Navigate to **Settings** → **Environment variables**
2. Add variables under **Build variables and secrets**
3. These are accessible during build, NOT at runtime

**Via wrangler.toml:**
```toml
name = "my-worker"

[vars]
API_HOST = "example.com"
API_ACCOUNT_ID = "example_user"
SERVICE_X_DATA = { URL = "service-x-api.dev.example", MY_ID = 123 }
```

**Via wrangler.jsonc:**
```json
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "vars": {
    "API_HOST": "example.com",
    "API_ACCOUNT_ID": "example_user",
    "SERVICE_X_DATA": {
      "URL": "service-x-api.dev.example",
      "MY_ID": 123
    }
  }
}
```

### 5.2 Default System Variables

Automatically injected (can be overridden):

| Variable | Value | Use Case |
|----------|-------|----------|
| `CI` | `true` | Detect CI environment |
| `WORKERS_CI` | `1` | Detect Workers Builds specifically |
| `WORKERS_CI_BUILD_UUID` | `<build-uuid>` | Pass to custom workflows |
| `WORKERS_CI_COMMIT_SHA` | `<commit-sha>` | Error reporting (e.g., Sentry) |
| `WORKERS_CI_BRANCH` | `<branch-name>` | Conditional logic per branch |

---

## 6. Monitoring and Troubleshooting

### 6.1 View Build Status

**Steps:**
1. Navigate to Worker in dashboard
2. Go to **Deployments** tab
3. Click **View build history** at bottom
4. Select build to view logs

### 6.2 Build Success Flow

```
Push to Git → Build triggered → Build succeeds → Version created → Auto-deployed (if configured)
```

**Verification:**
- Check **Version History** for new version
- Find **Preview URL** under Version ID
- Test at `<worker-name>.workers.dev`

### 6.3 Common Issues

**Build fails with "Worker name mismatch":**
- Ensure dashboard Worker name matches `wrangler.toml` `name` field

**Build fails with "API token error":**
- Verify token has required permissions
- Check token hasn't expired

**Build succeeds but not deployed:**
- Check deploy command is `npx wrangler deploy` (not `versions upload`)
- Verify branch is production branch

---

## 7. Disconnecting Builds

### 7.1 Disconnect Repository

**Steps:**
1. Navigate to Worker → **Settings** → **Builds**
2. Click **Disconnect**
3. Confirm disconnection

### 7.2 Switch Repository

**Steps:**
1. Disconnect current repository (see 7.1)
2. Reconnect to new repository (see 2.2)

### 7.3 Disable Auto-Deploy (Keep Builds)

**To create versions without auto-deploying:**
- Change deploy command to: `npx wrangler versions upload`
- Builds will create versions but not promote to active deployment

---

## 8. Best Practices

### 8.1 Repository Structure
```
my-worker/
├── src/
│   └── index.js
├── public/              # Static assets (optional)
├── wrangler.toml        # Worker configuration
├── package.json         # Dependencies
└── .github/
    └── workflows/       # Optional: external CI/CD
```

### 8.2 Wrangler Configuration Template

**Minimal wrangler.toml:**
```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"
```

**With assets:**
```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"
assets = { directory = "./public" }
```

### 8.3 Security
- Never commit API tokens to repository
- Use build secrets for sensitive values
- Rotate API tokens regularly
- Use least-privilege permissions

### 8.4 Deployment Strategy
- Use `main` branch for production
- Use feature branches with `versions upload` for previews
- Test preview URLs before merging
- Monitor build logs for warnings

---

## 9. Quick Reference

### 9.1 Common Commands

```bash
# Standard deployment
npx wrangler deploy

# Create version without deploying
npx wrangler versions upload

# Deploy with environment
npx wrangler deploy --env production

# Deploy with assets
npx wrangler deploy --assets ./public
```

### 9.2 Dashboard URLs

- **Workers Dashboard:** https://dash.cloudflare.com/?to=/:account/workers-and-pages
- **API Tokens:** My Profile → API Tokens
- **Build Settings:** Worker → Settings → Builds
- **Environment Variables:** Worker → Settings → Environment variables

### 9.3 Support Resources

- **Documentation:** https://developers.cloudflare.com/workers/ci-cd/builds/
- **Configuration Guide:** https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- **Troubleshooting:** https://developers.cloudflare.com/workers/ci-cd/builds/troubleshoot/

---

## 10. Checklist

### Pre-Deployment
- [ ] `wrangler.toml` configured with correct `name`
- [ ] Wrangler added to `package.json` dependencies
- [ ] Worker tested locally with `wrangler dev`
- [ ] API token created with required permissions
- [ ] Environment variables configured (if needed)

### Initial Setup
- [ ] Repository connected to Worker
- [ ] Build settings configured
- [ ] Deploy command verified
- [ ] First build triggered and successful
- [ ] Worker accessible at `.workers.dev` URL

### Post-Deployment
- [ ] Build logs reviewed for warnings
- [ ] Worker functionality tested
- [ ] Preview URLs working for non-prod branches
- [ ] Monitoring configured (optional)

---

**Document Control:**
- **Owner:** DevOps Team
- **Review Cycle:** Quarterly
- **Next Review:** 2026-04-26

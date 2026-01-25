# Cloudflare GitHub Secrets Setup

## Required Secrets

Add these to your GitHub repository secrets:

### 1. Get Cloudflare API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use template: "Edit Cloudflare Workers"
4. Or create custom token with permissions:
   - Account > Workers Scripts > Edit
5. Copy the token

### 2. Get Cloudflare Account ID

1. Go to https://dash.cloudflare.com/
2. Select any domain (or Workers & Pages)
3. Account ID is in the right sidebar
4. Or find it in URL: `dash.cloudflare.com/<ACCOUNT_ID>/...`

### 3. Add to GitHub Secrets

1. Go to: https://github.com/meta-introspector/meta-meme/settings/secrets/actions
2. Click "New repository secret"
3. Add:
   - Name: `CLOUDFLARE_API_TOKEN`
   - Value: (your API token from step 1)
4. Click "Add secret"
5. Repeat for:
   - Name: `CLOUDFLARE_ACCOUNT_ID`
   - Value: (your account ID from step 2)

## Test Deployment

After adding secrets, push to trigger deployment:

```bash
git add .github/workflows/cloudflare.yml
git commit -m "Add Cloudflare auto-deploy"
git push origin unified-memes
```

Check deployment at:
- GitHub Actions: https://github.com/meta-introspector/meta-meme/actions
- Cloudflare Dashboard: https://dash.cloudflare.com/

## Expected Worker URL

After successful deployment:
```
https://meta-meme.YOUR_SUBDOMAIN.workers.dev
```

Find exact URL in Cloudflare Dashboard → Workers & Pages → meta-meme

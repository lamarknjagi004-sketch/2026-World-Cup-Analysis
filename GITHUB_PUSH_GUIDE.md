# GitHub Push Instructions

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in to your account
2. Click the **+** icon in the top-right corner and select **New repository**
3. Name your repository: `2026-world-cup-predictor`
4. Add description: `Advanced Machine Learning & Statistical Sports Analytics for 2026 FIFA World Cup`
5. Choose visibility: **Public** (or Private if you prefer)
6. **DO NOT** initialize with README, .gitignore, or license (files already exist locally)
7. Click **Create repository**

## Step 2: Connect GitHub Repository

After creating the repository, GitHub will show you commands. Copy the HTTPS or SSH URL from the "Quick setup" section, then run:

```bash
git remote add origin https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor.git
```

**OR if you use SSH:**

```bash
git remote add origin git@github.com:lamarknjagi004-sketch/2026-world-cup-predictor.git
```

To verify the remote was added:
```bash
git remote -v
```

You should see:
```
origin  https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor.git (fetch)
origin  https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor.git (push)
```

## Step 3: Set the Default Branch

```bash
git branch -M main
```

## Step 4: Push Your Code

```bash
git push -u origin main
```

**First time push**: You may be asked to authenticate with your GitHub credentials.

---

## Authentication Methods

### Option A: HTTPS (Easier for beginners)
When prompted, use your GitHub username and a Personal Access Token (PAT):

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create a new token with `repo` permissions
3. Use token as password when pushing

### Option B: SSH (More secure)
```bash
# Generate SSH key (if you haven't already)
ssh-keygen -t ed25519 -C "lamarknjagi004@gmail.com"

# Add SSH key to GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste the public key content
```

---

## After First Push

Once your code is on GitHub, you can:

1. **Clone it elsewhere:**
   ```bash
   git clone https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor.git
   ```

2. **Make changes locally and push:**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

3. **View on GitHub:** https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor

---

## Troubleshooting

### "fatal: '#origin' does not appear to be a 'git' repository"
You haven't added the remote. Run the command from Step 2 first.

### Authentication failed
- For HTTPS: Use a Personal Access Token, not your password
- For SSH: Ensure your SSH key is added to GitHub and configured locally

### Permission denied (publickey)
You need to set up SSH keys. Follow Option B above.

---

## Next Steps

1. Complete the 4 steps above
2. Your repository will be live on GitHub
3. You can now add collaborators, create issues, manage branches, etc.
4. Share the repository URL with others

**Repository URL (after setup):** 
`https://github.com/lamarknjagi004-sketch/2026-world-cup-predictor`

---

Need help with any step? Follow the prompts and let me know if you encounter issues!

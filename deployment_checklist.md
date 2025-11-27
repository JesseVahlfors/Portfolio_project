# 🚀 Deployment Checklist (Django + Tailwind + Render)

A simple checklist to use before pushing updates to production.  
Follow this to avoid common deployment issues with migrations, static files, and Tailwind builds.

---

## 0. If working on a feature branch — merge it before deploy

Make sure your feature branch is fully merged into `main` before pushing to production.

1. Switch to main:

        git switch main

2. Pull the latest changes:

        git pull

3. Merge your feature branch into main:

        git merge feature/your-branch-name

4. Push main to GitHub:

        git push

After this, continue with the normal deployment steps below.

## 1. Update Virtual Environment (optional)

If you installed or updated dependencies:

    pip freeze > requirements.txt

Then commit the updated `requirements.txt`.

---

## 2. Run Migrations Locally

Before pushing anything:

    python manage.py makemigrations
    python manage.py migrate

- Confirm new migration files were created.  
- Verify that all migrations apply cleanly.  
- Commit migration files with your other changes.

---

## 3. Run the Development Server

    python manage.py runserver

Check the following:

- Project list page loads correctly  
- Project detail pages load (hero, summary, HTML content)  
- Profile/About pages render correctly  
- Images load  
- No missing template variables  
- No Django errors in console  

---

## 4. Build Tailwind CSS (locally)

    python manage.py tailwind build

Verify:

- No Tailwind errors  
- CSS updates appear in dev mode  
- No missing classes or purge issues  

(Even if Render builds Tailwind automatically, this step catches issues early.)

---

## 5. Collect Static Files

    python manage.py collectstatic --noinput

Check:

- Static files collect successfully  
- No path or configuration errors  

---

## 6. Commit All Changes

    git add .
    git commit -m "deploy: update models, migrations, templates, and static build"
    git push

Ensure you included:

- Model updates  
- Migration files  
- Template changes  
- Static files (if tracked)  
- Tailwind build output (if tracked) 

---
## 7. Deploy to Production (Render)

Render will:

1. Pull your latest commit  
2. Install dependencies  
3. Run your build command  
4. Apply migrations (if configured)  
5. Start your Django server  

After deployment completes, visit your production site and verify:

- Pages load without errors  
- Styles look correct (Tailwind built correctly)  
- Static files load (no 404s)  
- New project content appears as expected  

---

## 8. Optional: Post-Deploy Checklist

For extra safety:

- Test the live website on desktop + mobile  
- Test any new links you added (GitHub, live link, PyPI URL)  
- Confirm project slugs work  
- Ensure Django Admin loads properly  

---

## ✨ Notes

- Always commit migrations together.  
- Use `blank=True` for optional model fields to keep admin/forms clean.  
- Tailwind build + `collectstatic` are the most common causes of missing styles.  
- If deployment fails, check logs first for:  
  - Missing environment variables  
  - Missing migrations  
  - Tailwind build errors  
  - `collectstatic` errors  
  - Import errors  

---

Happy deploying! 🚀

# 🚀 Emerald Zambrut Portfolio - Development & Deployment Guide

## 📁 Project Structure

```
src/
├── assets/              # Static assets (CSS, images, fonts)
│   └── css/
│       └── index.css    # Main stylesheet with Emerald Zambrut theme
├── components/          # Reusable components
│   ├── layout/         # Layout components (Container, Section)
│   └── ui/             # UI components (Button, Card)
├── composables/         # Vue composables (state logic)
│   ├── useCustomCursor.ts
│   ├── useIntersectionObserver.ts
│   ├── useLazyImage.ts
│   ├── useScrollReveal.ts
│   ├── useSeo.ts
│   ├── useTheme.ts
│   └── useThemeEnhanced.ts
├── constants/           # Application constants
│   └── index.ts
├── data/                # JSON data files
│   ├── about.json
│   ├── blog/
│   ├── contact.json
│   ├── global.json
│   ├── home.json
│   └── projects.json
├── features/            # Feature-based components
│   ├── home/
│   ├── projects/
│   └── ...
├── lib/                 # Third-party wrappers
├── pages/               # Nuxt pages (auto-routed)
│   ├── index.vue
│   ├── about/
│   ├── projects/
│   └── ...
├── types/               # TypeScript definitions
│   └── index.ts
└── utils/               # Utility functions
    └── index.ts
```

## 🛠️ Development

### Prerequisites
- Node.js 18+ 
- pnpm or npm

### Setup
```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Generate static site (for GitHub Pages)
pnpm generate

# Preview production build
pnpm preview
```

## 🌐 GitHub Pages Deployment

### Option 1: Manual Deployment

1. **Generate static files:**
```bash
pnpm generate
```

2. **Deploy to GitHub Pages:**
```bash
# Using gh-pages package
pnpm add -D gh-pages

# Deploy dist folder to gh-pages branch
pnpm exec gh-pages -d dist
```

### Option 2: GitHub Actions (Recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install

      - name: Build
        run: pnpm generate

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Configuration for GitHub Pages

If deploying to `username.github.io/repo-name`:

1. Update `nuxt.config.ts`:
```typescript
app: {
  baseURL: '/repo-name/',
  buildAssetsDir: '/_nuxt/'
}
```

2. Or set environment variable:
```bash
export NUXT_APP_BASE_URL=/repo-name/
pnpm generate
```

## 🎨 Design System

### Color Palette (Emerald Zambrut)
- **Brand**: `#00DC82` (Emerald Green)
- **Brand Light**: `#34FDA3`
- **Brand Dark**: `#059669`
- **Surface**: Dynamic based on theme
- **Background**: Mesh gradient with emerald tones

### Typography
- **Primary**: Plus Jakarta Sans
- **Display**: Space Grotesk

### Components

#### Button
```vue
<Button variant="primary" size="lg">
  Click Me
</Button>

<!-- Variants: primary, secondary, outline, ghost, danger -->
<!-- Sizes: sm, md, lg -->
```

#### Card
```vue
<Card>
  <h3>Card Title</h3>
  <p>Card content with spotlight effect</p>
</Card>
```

#### Section
```vue
<Section>
  <Container>
    <h2>Section Title</h2>
    <!-- Content -->
  </Container>
</Section>
```

## 🔧 Customization

### Adding New Pages
1. Create file in `src/pages/`
2. Use `useSeoMeta` for SEO
3. Import from constants and types

### Adding Data
Edit JSON files in `src/data/` or create new ones.

### Extending Types
Add interfaces to `src/types/index.ts`

## 📊 Performance Optimization

### Image Optimization
- Use WebP/AVIF formats
- Implement lazy loading with `useLazyImage`
- Add responsive srcset

### Code Splitting
- Automatic with Nuxt
- Manual chunks configured in `nuxt.config.ts`

### SEO Best Practices
- Meta tags on every page
- Structured data (JSON-LD)
- Sitemap generation
- Open Graph tags

## 🚨 Troubleshooting

### Build Errors
```bash
# Clear cache
rm -rf .nuxt dist node_modules
pnpm install
pnpm generate
```

### GitHub Pages 404
- Ensure `baseURL` is correct
- Check that all routes are prerendered
- Verify asset paths start with `/`

### Theme Not Working
- Check localStorage key: `emerald-zambrut-theme`
- Verify dark class on html element

## 📝 Contributing

1. Follow TypeScript strict mode
2. Use composables for state logic
3. Keep components small and focused
4. Document new features
5. Test on mobile and desktop

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ using Nuxt 3, Vue 3, TailwindCSS, and Three.js**

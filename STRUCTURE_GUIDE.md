# 📁 Struktur Folder Portfolio - Emerald Zambrut

## Struktur yang Direkomendasikan

```
src/
├── assets/           # Static files (css, images, fonts, icons)
├── components/       # Reusable UI components
│   ├── ui/          # Base components (Button, Card, Input)
│   └── layout/      # Layout components (Container, Grid, Section)
├── composables/     # Vue composables (useTheme, useScrollReveal)
├── constants/       # App constants (routes, socials, config)
├── data/            # Content data (JSON, Markdown)
├── features/        # Feature-based modules
│   ├── home/        # Homepage components
│   ├── about/       # About page components
│   ├── projects/    # Projects components
│   ├── gallery/     # Gallery components
│   └── contact/     # Contact components
├── pages/           # Route pages (Nuxt auto-routing)
├── types/           # TypeScript definitions
└── utils/           # Helper functions
```

## Prinsip Arsitektur

### 1. Feature-Based Organization
- Setiap fitur di folder terpisah (`src/features/*`)
- Komponen spesifik fitur ada di dalam folder fitur
- Mudah di-maintain dan di-scale

### 2. Component Hierarchy
- **Base** (`components/ui/`): Generik, tanpa business logic
- **Layout** (`components/layout/`): Struktur reusable  
- **Feature** (`features/*/ `): Business logic spesifik
- **Page** (`pages/`): Route-level components

### 3. Data Flow
```
Pages → Features → Components → Composables
  ↓         ↓          ↓           ↓
Data     Logic      UI State   Shared Logic
```

## Konvensi Penamaan

| Tipe | Format | Contoh |
|------|--------|--------|
| Components | PascalCase | `ProjectCard.vue` |
| Composables | camelCase + `use` | `useTheme.ts` |
| Utils | camelCase | `formatDate.ts` |
| Constants | camelCase | `techStack.ts` |
| Types | PascalCase | `Project.ts` |

## Best Practices

✅ **DO:**
- Komponen kecil & fokus (max 200 baris)
- Lazy load heavy components
- Gunakan TypeScript untuk type safety
- Extract logic ke composables
- Optimize images (WebP/AVIF)

❌ **DON'T:**
- Komponen terlalu besar (>500 baris)
- Business logic di pages
- Hardcode values (gunakan constants)
- Import semua icon (lazy load)

---

**Design System**: Emerald Zambrut  
**Framework**: Nuxt 4 + Vue 3 + Tailwind CSS

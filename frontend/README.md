# 🎨 Daily Notes Frontend

Vue.js frontend application built with Nuxt.js for the Daily Notes project.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm/yarn/pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server (runs on http://localhost:3000)
npm run dev
```

## 🛠️ Tech Stack

- **Nuxt.js 3** - Vue.js framework with SSR capabilities
- **Vue 3** - Progressive JavaScript framework  
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - Promise-based HTTP client
- **Vue Composition API** - Modern Vue.js reactive system

## 📁 Project Structure

```
frontend/
├── app.vue                 # Root application component
├── nuxt.config.ts         # Nuxt configuration
├── components/            # Reusable Vue components
│   ├── Footer.vue         # Application footer
│   ├── Navbar.vue         # Navigation bar with auth
│   └── NoteCard.vue       # Note display/edit component
├── composables/           # Vue composables
│   └── useAuth.js         # Authentication logic
├── layouts/               # Application layouts
│   └── default.vue        # Default page layout
├── middleware/            # Route middleware
│   └── auth.js            # Authentication middleware
├── pages/                 # File-based routing
│   ├── index.vue          # Home page (redirects)
│   ├── login.vue          # Login page
│   ├── register.vue       # Registration page
│   └── dashboard.vue      # Main notes dashboard
├── plugins/               # Nuxt plugins
│   └── auth.client.js     # Client-side auth plugin
└── assets/                # Static assets
    └── css/
        └── main.css       # Global styles
```

## 🎯 Key Features

### 🔐 Authentication
- **Login/Register Forms** - User-friendly authentication
- **JWT Token Management** - Automatic token handling
- **Route Protection** - Middleware-based access control
- **Auto-logout** - Handle expired tokens gracefully

### 📝 Note Management
- **CRUD Operations** - Create, read, update, delete notes
- **Inline Editing** - Edit notes directly in place
- **Real-time Updates** - Instant UI feedback
- **Responsive Design** - Mobile-friendly interface

### ⚡ User Experience
- **Loading States** - Visual feedback during operations
- **Error Handling** - User-friendly error messages
- **Keyboard Shortcuts** - Power user features
- **Smooth Transitions** - Modern UI interactions

## 🧩 Components

### NoteCard.vue
Interactive note component with inline editing capabilities:
- **View Mode** - Display note title, content, and timestamp
- **Edit Mode** - Inline editing with save/cancel options
- **Actions** - Edit and delete buttons
- **Keyboard Support** - Enter to save, Esc to cancel

### Navbar.vue
Responsive navigation with authentication state:
- **Brand Logo** - Application title/link
- **Auth Links** - Login/Register when logged out
- **User Info** - Username display when logged in
- **Logout Button** - Secure logout functionality

### useAuth Composable
Centralized authentication logic:
- **State Management** - User and token state
- **API Calls** - Login, logout, user fetching
- **Local Storage** - Persistent authentication
- **Error Handling** - Authentication error management

## 🔧 Configuration

### Nuxt Config (`nuxt.config.ts`)
```typescript
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

### API Integration
The frontend communicates with the Flask backend at `http://localhost:5001`:

```javascript
// Example API call
const response = await axios.get('http://localhost:5001/api/notes', {
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})
```

## 🎨 Styling

### Tailwind CSS
Utility-first CSS framework for rapid UI development:
- **Responsive Design** - Mobile-first approach
- **Component Classes** - Reusable style patterns
- **Color Scheme** - Professional blue/gray palette
- **Typography** - Consistent text styling

### Key Style Patterns
```css
/* Buttons */
.btn-primary { @apply bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600; }
.btn-danger { @apply bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600; }

/* Cards */
.card { @apply bg-white p-4 shadow rounded mb-3; }

/* Forms */
.form-input { @apply w-full p-2 border rounded; }
```

## 🔄 State Management

### Authentication State
```javascript
// Reactive authentication state
const token = ref('')
const user = ref(null)
const isAuthenticated = computed(() => !!token.value)
```

### Note Management
```javascript
// Dashboard component state
const notes = ref([])
const isLoading = ref(false)
const isCreating = ref(false)
```

## 🚦 Routing & Middleware

### File-based Routing
- `/` → `pages/index.vue` (redirects to login)
- `/login` → `pages/login.vue`
- `/register` → `pages/register.vue`
- `/dashboard` → `pages/dashboard.vue` (protected)

### Auth Middleware
```javascript
// middleware/auth.js
export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated, initAuth } = useAuth()
  initAuth()
  
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
```

## 🔧 Development Commands

```bash
# Development
npm run dev              # Start dev server with hot reload

# Building
npm run build           # Build for production
npm run preview         # Preview production build

# Linting & Formatting
npm run lint            # Run ESLint
npm run lint:fix        # Fix ESLint errors
npm run format          # Format with Prettier

# Type Checking
npm run typecheck       # Run TypeScript checks
```

## 🐛 Troubleshooting

### Common Issues

**Backend connection failed**
- Ensure Flask backend is running on port 5001
- Check CORS configuration
- Verify API endpoints are accessible

**Authentication issues**
- Clear browser localStorage
- Check JWT token validity
- Verify backend authentication routes

**UI not updating**
- Check Vue reactivity
- Verify component key attributes
- Ensure proper event emission

**Styling issues**
- Check Tailwind CSS compilation
- Verify class names are correct
- Ensure styles are not being overridden

## 📱 Mobile Responsiveness

The application is fully responsive and works on:
- **Desktop** - Full-featured experience
- **Tablet** - Optimized layout
- **Mobile** - Touch-friendly interface

### Responsive Breakpoints
```css
/* Tailwind CSS breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
```

For more information, check the main project README in the root directory.

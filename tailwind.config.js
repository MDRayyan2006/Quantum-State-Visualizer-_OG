/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        quantum: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          border: '#1e293b',
          darker: '#0f172a',
          dark: '#1e293b',
          light: '#64748b',
          cyan: '#00ffff',
          green: '#00ff88',
          red: '#ff4757',
          blue: '#0ea5e9',
        },
        neon: {
          blue: '#00ffff',
          green: '#00ff88',
          pink: '#ff0080',
          purple: '#8000ff',
          yellow: '#ffff00',
        },
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        }
      },
      animation: {
        'quantum-pulse': 'quantum-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'quantum-float': 'quantum-float 6s ease-in-out infinite',
        'quantum-glow': 'quantum-glow 2s ease-in-out infinite alternate',
        'quantum-spin': 'quantum-spin 3s linear infinite',
      },
      keyframes: {
        'quantum-pulse': {
          '0%, 100%': {
            opacity: '1',
          },
          '50%': {
            opacity: '.5',
          },
        },
        'quantum-float': {
          '0%, 100%': {
            transform: 'translateY(0px)',
          },
          '50%': {
            transform: 'translateY(-20px)',
          },
        },
        'quantum-glow': {
          '0%': {
            boxShadow: '0 0 5px #00ff88, 0 0 10px #00ff88, 0 0 15px #00ff88',
          },
          '100%': {
            boxShadow: '0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88',
          },
        },
        'quantum-spin': {
          '0%': {
            transform: 'rotate(0deg)',
          },
          '100%': {
            transform: 'rotate(360deg)',
          },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      fontFamily: {
        'quantum': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}

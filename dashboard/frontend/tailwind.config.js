/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cyberpunk Neon Color Palette
        'neon-cyan': '#00F5FF',
        'neon-pink': '#FF006E',
        'neon-purple': '#9D4EDD',
        'neon-green': '#39FF14',
        'neon-yellow': '#FFD60A',

        border: 'rgba(0, 245, 255, 0.2)',
        input: "hsl(var(--input))",
        ring: "#00F5FF",
        background: '#0A0E27',
        foreground: '#E0E7FF',
        primary: {
          DEFAULT: '#00F5FF',
          foreground: '#0A0E27',
        },
        secondary: {
          DEFAULT: '#9D4EDD',
          foreground: '#E0E7FF',
        },
        destructive: {
          DEFAULT: '#FF006E',
          foreground: '#E0E7FF',
        },
        muted: {
          DEFAULT: '#2A2F4A',
          foreground: '#9CA3AF',
        },
        accent: {
          DEFAULT: '#FF006E',
          foreground: '#E0E7FF',
        },
        card: {
          DEFAULT: 'rgba(26, 31, 58, 0.6)',
          foreground: '#E0E7FF',
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 245, 255, 0.5), 0 0 40px rgba(0, 245, 255, 0.3)',
        'neon-pink': '0 0 20px rgba(255, 0, 110, 0.5), 0 0 40px rgba(255, 0, 110, 0.3)',
        'neon-purple': '0 0 20px rgba(157, 78, 221, 0.5), 0 0 40px rgba(157, 78, 221, 0.3)',
        'cyber-card': '0 8px 32px 0 rgba(0, 245, 255, 0.1)',
      },
      backgroundImage: {
        'cyber-grid': "linear-gradient(rgba(0, 245, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 245, 255, 0.1) 1px, transparent 1px)",
      },
      backgroundSize: {
        'cyber-grid': '50px 50px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(0, 245, 255, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 245, 255, 0.6)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
      },
    },
  },
  plugins: [],
}

import { useEffect, useRef } from 'react'

interface MatrixRainbowProps {
  active: boolean
  opacity?: number
  speed?: number
}

const MatrixRainbow = ({
  active,
  opacity = 0.3,
  speed = 1
}: MatrixRainbowProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!active) return

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const updateSize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    updateSize()
    window.addEventListener('resize', updateSize)

    // Matrix characters (Katakana + symbols)
    const chars = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ█▓░▒║│┃╽╿┇┊┋'
    const charArray = chars.split('')

    // Rainbow colors
    const rainbowColors = [
      '#06b6d4', // Cyan
      '#3b82f6', // Blue
      '#8b5cf6', // Purple
      '#ec4899', // Pink
      '#f59e0b', // Orange
      '#10b981', // Green
    ]

    // Column setup
    const fontSize = 14
    const columns = Math.floor(canvas.width / fontSize)
    const drops: number[] = []
    const colors: string[] = []
    const speeds: number[] = []

    // Initialize drops
    for (let i = 0; i < columns; i++) {
      drops[i] = Math.random() * -100
      colors[i] = rainbowColors[Math.floor(Math.random() * rainbowColors.length)]
      speeds[i] = (0.3 + Math.random() * 0.7) * speed
    }

    // Draw function
    const draw = () => {
      // Fade effect
      ctx.fillStyle = 'rgba(15, 23, 42, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.font = `${fontSize}px monospace`

      // Draw characters
      for (let i = 0; i < drops.length; i++) {
        const char = charArray[Math.floor(Math.random() * charArray.length)]

        // Leading character (brightest)
        ctx.fillStyle = colors[i]
        ctx.globalAlpha = 1
        ctx.fillText(char, i * fontSize, drops[i] * fontSize)

        // Trail effect
        for (let j = 1; j < 10; j++) {
          const trailY = (drops[i] - j) * fontSize
          if (trailY > 0) {
            ctx.globalAlpha = 1 - (j * 0.1)
            ctx.fillText(
              charArray[Math.floor(Math.random() * charArray.length)],
              i * fontSize,
              trailY
            )
          }
        }

        // Move drop
        drops[i] += speeds[i]

        // Reset when reaches bottom
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
          if (Math.random() > 0.7) {
            colors[i] = rainbowColors[Math.floor(Math.random() * rainbowColors.length)]
          }
        }
      }

      ctx.globalAlpha = 1
    }

    const interval = setInterval(draw, 33) // ~30 FPS

    return () => {
      clearInterval(interval)
      window.removeEventListener('resize', updateSize)
    }
  }, [active, opacity, speed])

  if (!active) return null

  return (
    <canvas
      ref={canvasRef}
      className="matrix-rainbow-canvas"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 0,
        opacity,
      }}
    />
  )
}

export default MatrixRainbow

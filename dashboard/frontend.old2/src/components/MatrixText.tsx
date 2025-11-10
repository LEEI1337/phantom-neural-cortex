import { useEffect, useState } from 'react'

interface MatrixTextProps {
  text: string
  duration?: number
  className?: string
}

const MatrixText = ({
  text,
  duration = 2000,
  className = ''
}: MatrixTextProps) => {
  const [displayText, setDisplayText] = useState('')
  const [isDecrypting, setIsDecrypting] = useState(true)

  useEffect(() => {
    const chars = 'ｱｲｳｴｵｶｷｸｹｺ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ█▓░▒'
    const finalText = text
    const steps = 20
    let currentStep = 0

    const interval = setInterval(() => {
      if (currentStep < steps) {
        let randomText = ''
        for (let i = 0; i < finalText.length; i++) {
          if (Math.random() < currentStep / steps) {
            randomText += finalText[i]
          } else {
            randomText += chars[Math.floor(Math.random() * chars.length)]
          }
        }
        setDisplayText(randomText)
        currentStep++
      } else {
        setDisplayText(finalText)
        setIsDecrypting(false)
        clearInterval(interval)
      }
    }, duration / steps)

    return () => clearInterval(interval)
  }, [text, duration])

  return (
    <span className={`matrix-text ${isDecrypting ? 'decrypting' : 'decrypted'} ${className}`}>
      {displayText}
    </span>
  )
}

export default MatrixText

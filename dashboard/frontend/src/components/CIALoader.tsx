import { useEffect, useState } from 'react'

interface CIALoaderProps {
  messages?: string[]
  onComplete?: () => void
}

const DEFAULT_MESSAGES = [
  'INITIALIZING QUANTUM MATRIX...',
  'DECRYPTING NEURAL PATHWAYS...',
  'ESTABLISHING SECURE CONNECTION...',
  'ANALYZING SWARM TOPOLOGY...',
  'OPTIMIZING HRM PARAMETERS...',
  'CALIBRATING AGENT SWITCHES...',
  'APPLYING CONFIGURATION...',
  'BROADCASTING TO NODES...',
  '>> SUCCESS: ALL SYSTEMS OPTIMAL <<',
]

const CIALoader = ({
  messages = DEFAULT_MESSAGES,
  onComplete
}: CIALoaderProps) => {
  const [lines, setLines] = useState<string[]>([])

  useEffect(() => {
    let currentIndex = 0

    const interval = setInterval(() => {
      if (currentIndex < messages.length) {
        setLines(prev => [...prev, messages[currentIndex]])
        currentIndex++
      } else {
        clearInterval(interval)
        if (onComplete) {
          setTimeout(onComplete, 500)
        }
      }
    }, 300)

    return () => clearInterval(interval)
  }, [messages, onComplete])

  return (
    <div className="cia-loader">
      {lines.map((line, index) => (
        <div
          key={index}
          className="cia-line"
          style={{
            animation: `fadeInGlitch 0.3s ease-out`,
            animationDelay: `${index * 0.1}s`,
            animationFillMode: 'backwards'
          }}
        >
          <span className="cia-prompt">{'>'}</span>
          <span className="cia-text rainbow-text-animated">
            {line}
          </span>
          {index === lines.length - 1 && (
            <span className="cursor-blink">█</span>
          )}
        </div>
      ))}
    </div>
  )
}

export default CIALoader

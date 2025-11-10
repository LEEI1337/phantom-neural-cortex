interface GlitchRainbowTextProps {
  text: string
  intensity?: 'low' | 'medium' | 'high'
  className?: string
}

const GlitchRainbowText = ({
  text,
  intensity = 'medium',
  className = ''
}: GlitchRainbowTextProps) => {
  return (
    <div
      className={`glitch-rainbow glitch-${intensity} ${className}`}
      data-text={text}
    >
      {text}
    </div>
  )
}

export default GlitchRainbowText

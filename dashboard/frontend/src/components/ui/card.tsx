import * as React from 'react'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className = '', ...props }: CardProps) {
  return (
    <div
      className={`bg-card text-card-foreground rounded-lg border border-border shadow-sm ${className}`}
      {...props}
    />
  )
}

export function CardHeader({ className = '', ...props }: CardProps) {
  return <div className={`p-6 pb-3 ${className}`} {...props} />
}

export function CardTitle({
  className = '',
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={`text-lg font-semibold leading-none ${className}`} {...props} />
}

export function CardDescription({
  className = '',
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={`text-sm text-muted-foreground mt-1.5 ${className}`} {...props} />
}

export function CardContent({ className = '', ...props }: CardProps) {
  return <div className={`p-6 pt-0 ${className}`} {...props} />
}

export function CardFooter({ className = '', ...props }: CardProps) {
  return <div className={`p-6 pt-0 flex items-center ${className}`} {...props} />
}

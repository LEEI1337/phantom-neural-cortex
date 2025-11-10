// Placeholder for tabs component (shadcn/ui style)
// In production, use actual shadcn/ui components

export function Tabs({ children, ...props }: any) {
  return <div {...props}>{children}</div>
}

export function TabsList({ children, ...props }: any) {
  return <div {...props}>{children}</div>
}

export function TabsTrigger({ children, ...props }: any) {
  return <button {...props}>{children}</button>
}

export function TabsContent({ children, ...props }: any) {
  return <div {...props}>{children}</div>
}

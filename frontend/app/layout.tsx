import type { ReactNode } from 'react';
export const metadata = { title: 'Coditude Task Demo', description: 'Next.js and FastAPI assessment demo' };
export default function RootLayout({children}: {children: ReactNode}) {return <html lang="en"><body style={{fontFamily:'Arial, sans-serif',maxWidth:700,margin:'50px auto',padding:20}}>{children}</body></html>}

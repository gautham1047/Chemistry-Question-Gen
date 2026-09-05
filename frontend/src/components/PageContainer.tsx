import React, { type ReactNode } from 'react';
import { Header } from './Header';

interface PageContainerProps {
  children: ReactNode;
  wide?: boolean;
  centered?: boolean;
  className?: string;
}

export const PageContainer: React.FC<PageContainerProps> = ({
  children,
  wide = false,
  centered = false,
  className = '',
}) => {
  const maxWidth = wide ? 'max-w-6xl' : 'max-w-5xl';
  const centerClass = centered ? 'flex flex-col justify-center' : '';

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />
      <main className={`flex-1 w-full mx-auto px-4 py-8 ${maxWidth} ${centerClass} ${className}`}>
        {children}
      </main>
    </div>
  );
};

export default PageContainer;
